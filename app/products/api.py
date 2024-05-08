from fastapi import APIRouter, Depends, HTTPException, Header

from .schema import SearchQuery, SearchResponse
from .service import ScrapeDentalStall

router = APIRouter()

STATIC_TOKEN = "static_token_here"


# Dependency to authenticate requests
def authenticate(token: str = Header(...)):
    if token != STATIC_TOKEN:
        raise HTTPException(status_code=401, detail="Invalid token")
    return True


@router.get("/search/", response_model=SearchResponse)
async def search(
    data: SearchQuery, authenticated: bool = Depends(authenticate)
):
    sds = ScrapeDentalStall(data)
    sds.scrape_and_save()
    return {"message": "scraped successfully"}
