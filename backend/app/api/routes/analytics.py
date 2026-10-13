from fastapi import APIRouter
from backend.app.schemas.analytics import (
    AnalyticsOverview,
    PriceAnalyticsResponse,
    AttributeBreakdown
)
from backend.app.services.analytics_service import analytics_service

router = APIRouter()

@router.get("/analytics/overview", response_model=AnalyticsOverview, tags=["Analytics"])
def get_analytics_overview():
    return analytics_service.get_overview()

@router.get("/analytics/prices", response_model=PriceAnalyticsResponse, tags=["Analytics"])
def get_price_analytics():
    return analytics_service.get_price_analytics()

@router.get("/analytics/attributes", response_model=AttributeBreakdown, tags=["Analytics"])
def get_attribute_analytics():
    return analytics_service.get_attribute_analytics()
