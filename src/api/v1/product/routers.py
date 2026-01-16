from fastapi import APIRouter

from .views import router as product_router

router = APIRouter(tags=["Product"])

router.include_router(product_router)