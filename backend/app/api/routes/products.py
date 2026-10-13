from fastapi import APIRouter, Query, HTTPException
from typing import Optional
from backend.app.schemas.product import ProductResponse, ProductListResponse
from backend.app.services.data_service import data_service

router = APIRouter()

@router.get("/products", response_model=ProductListResponse, tags=["Products"])
def list_products(
    category: Optional[str] = Query(None, description="Filter by product category"),
    subcategory: Optional[str] = Query(None, description="Filter by subcategory"),
    location: Optional[str] = Query(None, description="Market location filter"),
    min_price: Optional[float] = Query(None, ge=0, description="Minimum price in INR"),
    max_price: Optional[float] = Query(None, ge=0, description="Maximum price in INR"),
    material: Optional[str] = Query(None, description="Fabric material filter"),
    color: Optional[str] = Query(None, description="Color filter"),
    search: Optional[str] = Query(None, description="Free-text search in title, brand, fabric"),
    sort: Optional[str] = Query(None, description="Sort order: price_asc, price_desc, rating, reviews, opportunity"),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100)
):
    return data_service.get_products(
        category=category,
        subcategory=subcategory,
        location=location,
        min_price=min_price,
        max_price=max_price,
        material=material,
        color=color,
        search=search,
        sort=sort,
        page=page,
        page_size=page_size
    )

@router.get("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def get_product(product_id: str):
    product = data_service.get_product_by_id(product_id)
    if not product:
        raise HTTPException(status_code=404, detail=f"Product with ID '{product_id}' not found.")
    return product
