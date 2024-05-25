from fastapi import APIRouter, Depends

from app.authenticate import token_authenticate
from .schema import SearchQuery, SearchResponse
from .service import ScrapeDentalStall

router = APIRouter()


@router.get("/search/", response_model=SearchResponse, tags=["Scrape Data"])
async def search(
    params: SearchQuery = Depends(),
    authenticated: bool = Depends(token_authenticate),
):
    sds = ScrapeDentalStall(params)
    sds.scrape_and_save()
    return {
        "message": "scraped successfully",
        "data": []
    }
