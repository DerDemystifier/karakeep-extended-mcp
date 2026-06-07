import json
import os
from pathlib import Path

import httpx
from fastmcp import FastMCP
from fastmcp.server.providers.openapi import RouteMap, MCPType


def load_openapi_spec() -> dict:
    """
    Load the Karakeep OpenAPI spec from either:
      - KARAKEEP_OPENAPI_URL
      - KARAKEEP_OPENAPI_SPEC local file path
    """
    spec_url = os.getenv("KARAKEEP_OPENAPI_URL")
    if spec_url:
        return httpx.get(spec_url, timeout=30).json()

    # Check in the current directory
    with open(Path(__file__).parent / "karakeep-openapi-spec.json", "r") as f:
        return json.loads(f.read())


karakeep_base_url = os.environ["KARAKEEP_URL"].rstrip("/") + "/api/v1"
karakeep_token = os.environ["KARAKEEP_TOKEN"]

spec = load_openapi_spec()

client = httpx.AsyncClient(
    base_url=karakeep_base_url,
    headers={
        "Authorization": f"Bearer {karakeep_token}",
        "Accept": "application/json",
    },
    timeout=httpx.Timeout(60.0),
)

# Important:
# Do not expose the entire huge spec at first.
# Allow-list the Karakeep areas you actually want Claude to use.
route_maps = [
    # Exclude /bookmarks/{bookmarkId}/summarize
    RouteMap(pattern=r"^/bookmarks/[^/]+/summarize$", mcp_type=MCPType.EXCLUDE),
    # Exclude /bookmarks/{bookmarkId}/assets*
    RouteMap(pattern=r"^/bookmarks/[^/]+/assets(/.*)?$", mcp_type=MCPType.EXCLUDE),

    # Avoid dangerous/admin/binary-heavy endpoints by default.
    RouteMap(pattern=r"^/admin(/.*)?$", mcp_type=MCPType.EXCLUDE),
    RouteMap(pattern=r"^/backups(/.*)?$", mcp_type=MCPType.EXCLUDE),
    RouteMap(pattern=r"^/assets(/.*)?$", mcp_type=MCPType.EXCLUDE),

    # Core Karakeep API areas.
    RouteMap(pattern=r"^/bookmarks(/.*)?$", mcp_type=MCPType.TOOL),
    RouteMap(pattern=r"^/lists(/.*)?$", mcp_type=MCPType.TOOL),
    RouteMap(pattern=r"^/tags(/.*)?$", mcp_type=MCPType.TOOL),

    # Exclude everything else.
    RouteMap(mcp_type=MCPType.EXCLUDE),
]

mcp = FastMCP.from_openapi(
    openapi_spec=spec,
    client=client,
    name="karakeep-openapi",
    route_maps=route_maps,

    # Karakeep's responses may drift a little from the spec.
    # This avoids overly strict response validation failures.
    validate_output=False,
)

if __name__ == "__main__":
    mcp.run()
