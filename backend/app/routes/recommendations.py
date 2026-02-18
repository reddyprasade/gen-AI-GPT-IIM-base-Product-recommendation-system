from fastapi import APIRouter

from backend.app.schemas import RecommendationRequest, RecommendationResponse
from backend.app.services.recommender import get_recommendations

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


@router.post("", response_model=RecommendationResponse)
def recommend_products(payload: RecommendationRequest) -> RecommendationResponse:
    return get_recommendations(payload)
