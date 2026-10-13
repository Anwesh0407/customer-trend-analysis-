from fastapi import APIRouter
from typing import List, Dict, Any

router = APIRouter()

@router.get("/categories", tags=["Categories"])
def get_categories() -> Dict[str, Any]:
    return {
        "categories": [
            {
                "id": "womens_clothing",
                "name": "Women's Clothing",
                "icon": "shirt",
                "subcategories": [
                    {
                        "id": "kurtas_kurtis",
                        "name": "Kurtas & Kurtis",
                        "active": True,
                        "description": "Daily wear, office wear, and festive ethnic tunics",
                        "product_count": 20
                    },
                    {
                        "id": "sarees",
                        "name": "Sarees & Blouses",
                        "active": False,
                        "description": "Sambalpuri, Bomkai, and Handloom sarees",
                        "product_count": 0
                    },
                    {
                        "id": "ethnic_sets",
                        "name": "Kurta Sets & Salwars",
                        "active": False,
                        "description": "Matching kurta pant dupatta ensembles",
                        "product_count": 0
                    }
                ]
            }
        ],
        "regions": [
            {"id": "odisha", "name": "Odisha (Primary Focus)", "default": True},
            {"id": "eastern_india", "name": "Eastern India & Neighboring States", "default": False},
            {"id": "all_india", "name": "All India Marketplace", "default": False}
        ],
        "price_presets": [
            {"label": "Under ₹500", "value": 500},
            {"label": "₹500 — ₹1,000", "value": 1000},
            {"label": "Over ₹1,000", "value": 2000}
        ],
        "materials": ["All", "Cotton", "Rayon", "Chanderi", "Cotton Silk", "Khadi"],
        "colors": ["All", "Blue", "Maroon", "Black", "Green", "Yellow", "Pink", "White"]
    }
