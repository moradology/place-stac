from typing import Any, Dict, List, Optional

import orjson
from pydantic import BaseModel

from place.common.util import get_param_str, get_param_str_raw, orjson_dumps


class RenderConfig(BaseModel):
    """
    A class used to represent information convenient for accessing
    the rendered assets of a collection.

    The parameters stored by this class are not the only parameters
    by which rendering is possible or useful but rather represent the
    most convenient renderings for human consumption and preview.
    For example, if a TIF asset can be viewed as an RGB approximating
    normal human vision, parameters will likely encode this rendering.
    """

    render_params: Dict[str, Any]
    minzoom: int = 14
    assets: Optional[List[str]] = ["cog"]
    maxzoom: Optional[int] = 30
    mosaic_preview_zoom: Optional[int] = None
    mosaic_preview_coords: Optional[List[float]] = None

    def get_full_render_qs(self, collection: str, item: Optional[str] = None) -> str:
        """
        Return the full render query string, including the
        item, collection, render and assets parameters.
        """
        collection_part = f"collection={collection}" if collection else ""
        item_part = f"&item={item}" if item else ""
        asset_part = self.get_assets_params()
        render_part = self.get_render_params()

        return "".join([collection_part, item_part, asset_part, render_part])

    def get_full_render_qs_raw(self, collection: str, item: Optional[str] = None) -> str:
        """
        Return the full render query string, including the
        item, collection, render and assets parameters.
        """
        collection_part = f"collection={collection}" if collection else ""
        item_part = f"&item={item}" if item else ""
        asset_part = self.get_assets_params()
        render_part = self.get_render_params_raw()

        return "".join([collection_part, item_part, asset_part, render_part])

    def get_assets_params(self) -> str:
        """
        Convert listed assets to a query string format with multiple `asset` keys
            None -> ""
            [data1] -> "&asset=data1"
            [data1, data2] -> "&asset=data1&asset=data2"
        """
        assets = self.assets or []
        keys = ["&assets="] * len(assets)
        params = ["".join(item) for item in zip(keys, assets)]

        return "".join(params)

    def get_render_params_raw(self) -> str:
        return f"&{get_param_str_raw(self.render_params)}"

    def get_render_params(self) -> str:
        return f"&{get_param_str(self.render_params)}"

    class Config:
        json_loads = orjson.loads
        json_dumps = orjson_dumps


IVORY_COAST_CONFIG = RenderConfig(render_params={"asset_bidx": "cog|1,2,3"})

RENDER_CONFIGS = {
    "IvoryCoast-Abidjian-Adjame": IVORY_COAST_CONFIG
}

def get_render_config(collection_id: str) -> RenderConfig:
    return RENDER_CONFIGS[collection_id]