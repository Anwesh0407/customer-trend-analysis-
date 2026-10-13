from fastapi import APIRouter
from backend.app.schemas.recommendation import RecommendationResponse
from backend.app.services.recommendation_service import recommendation_service

router = APIRouter()

@router.get("/recommendations", response_model=RecommendationResponse, tags=["Recommendations"])
def get_recommendations():
    return recommendation_service.get_recommendations()
