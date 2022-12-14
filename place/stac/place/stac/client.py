import logging
from typing import Any, List, Type
from urllib.parse import urljoin

import attr
from fastapi import Request
from stac_fastapi.pgstac.core import CoreCrudClient
from stac_fastapi.pgstac.types.search import PgstacSearch
from stac_fastapi.types.search import BaseSearchPostRequest
from stac_fastapi.types.errors import NotFoundError
from stac_fastapi.types.stac import (
    Collection,
    Item,
    ItemCollection,
)

from place.common.render import get_render_config
from place.stac.links import LinkInjector

logger = logging.getLogger(__name__)


@attr.s
class PlaceClient(CoreCrudClient):
    """Client for core endpoints defined by stac."""

    def inject_collection_links(
        self, collection: Collection, request: Request
    ) -> Collection:
        """Add extra/non-mandatory links to a Collection"""
        collection_id = collection.get("id", "")
        render_config = get_render_config(collection_id)
        LinkInjector(collection_id, render_config, request).inject_collection(
            collection
        )

        return collection


    def inject_item_links(self, item: Item, request: Request) -> Item:
        """Add extra/non-mandatory links to an Item"""
        collection_id = item.get("collection", "")
        if collection_id:
            render_config = get_render_config(collection_id)
            LinkInjector(collection_id, render_config, request).inject_item(item)

        return item


    async def get_collection(self, collection_id: str, **kwargs: Any) -> Collection:
        """Get collection by id and inject PQE links.
        Called with `GET /collections/{collection_id}`.
        In the Planetary Computer, this method has been modified to inject
        links which facilitate users to accessing rendered assets and
        associated metadata.
        Args:
            collection_id: Id of the collection.
        Returns:
            Collection.
        """
        _super: CoreCrudClient = super()
        _request = kwargs["request"]

        try:
            result = await _super.get_collection(collection_id, **kwargs)
        except NotFoundError:
            raise NotFoundError(f"No collection with id '{collection_id}' found!")
        return self.inject_collection_links(result, _request)

    async def get_item(self, item_id: str, collection_id: str, **kwargs: Any) -> Item:
        _super: CoreCrudClient = super()
        _request = kwargs["request"]

        item = await _super.get_item(item_id, collection_id, **kwargs)
        return self.inject_item_links(item, _request)


    async def _search_base(
        self, search_request: PgstacSearch, **kwargs: Any
    ) -> ItemCollection:
        """Cross catalog search (POST).
        Called with `POST /search`.
        Args:
            search_request: search request parameters.
        Returns:
            ItemCollection containing items which match the search criteria.
        """
        _super: CoreCrudClient = super()
        request = kwargs["request"]

        result = await _super._search_base(search_request, **kwargs)

        item_collection = ItemCollection(
            **{
                **result,
                "features": [
                    self.inject_item_links(i, request)
                    for i in result.get("features", [])
                ],
            }
        )
        return item_collection

    @classmethod
    def create(
        cls,
        post_request_model: Type[BaseSearchPostRequest],
    ) -> "PlaceClient":
        it = cls(
            landing_page_id="place",
            title="PLACE STAC API",
            description="Spatiotemporal Asset Catalog managed by PLACE",
            post_request_model=post_request_model,
        )
        return it