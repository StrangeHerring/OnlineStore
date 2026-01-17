from fastapi import APIRouter

from .views import router as cart_router

router = APIRouter(tags=["Cart"])

router.include_router(cart_router)