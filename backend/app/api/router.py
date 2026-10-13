from fastapi import APIRouter
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.categories import router as categories_router
from backend.app.api.routes.products import router as products_router
from backend.app.api.routes.analytics import router as analytics_router
from backend.app.api.routes.reviews import router as reviews_router
from backend.app.api.routes.recommendations import router as recommendations_router
from backend.app.api.routes.assistant import router as assistant_router

api_router = APIRouter()

api_router.include_router(health_router)
api_router.include_router(categories_router)
api_router.include_router(products_router)
api_router.include_router(analytics_router)
api_router.include_router(reviews_router)
api_router.include_router(recommendations_router)
api_router.include_router(assistant_router)
