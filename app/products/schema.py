from typing import List, Optional

from fastapi import Query
from pydantic import BaseModel


class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str


class SearchQuery(BaseModel):
    page: Optional[int] = Query(1, description="Page number")
    proxy: Optional[str] = Query("", description="Proxy information")


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "Success"
    data: List[Product]
