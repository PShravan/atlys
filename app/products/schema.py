from typing import List, Optional

from pydantic import BaseModel


class Product(BaseModel):
    product_title: str
    product_price: float
    path_to_image: str


class SearchQuery(BaseModel):
    page: Optional[int] = 1
    proxy: Optional[str] = ""


class SearchResponse(BaseModel):
    status: bool = True
    message: str = "Success"
    data: List[Product]
