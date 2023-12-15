import os

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from starlette.responses import Response

from rio_tiler.profiles import img_profiles
from rio_tiler.io import Reader

origins = [
    "http://localhost:5173"
]

app = FastAPI(
    title="rio-tiler",
    description="A lightweight Cloud Optimized GeoTIFF tile server",
)

app.add_middleware(CORSMiddleware, allow_origins=origins, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

@app.get(
    r"/{z}/{x}/{y}.png",
    responses={
        200: {
            "content": {"image/png": {}}, "description": "Return an image.",
        }
    },
    response_class=Response,
    description="Read COG and return a tile",
)
def tile(
        z: int,
        x: int,
        y: int,
):
    """Handle tile requests."""
    with Reader("data/merge_cog.tif") as cog:
        img = cog.tile(x, y, z, nodata=0)
    content = img.render(img_format="PNG", **img_profiles.get("png"))
    return Response(content, media_type="image/png")


@app.get("/tilejson.json", responses={200: {"description": "Return a tilejson"}})
def tilejson(
        request: Request,
        url: str = Query(..., description="Cloud Optimized GeoTIFF URL."),
):
    """Return TileJSON document for a COG."""
    tile_url = str(request.url_for("tile", z="{z}", x="{x}", y="{y}"))
    tile_url = f"{tile_url}?url={url}"

    with Reader(url) as cog:
        return {
            "bounds": cog.geographic_bounds,
            "minzoom": cog.minzoom,
            "maxzoom": cog.maxzoom,
            "name": os.path.basename(url),
            "tiles": [tile_url],
        }
