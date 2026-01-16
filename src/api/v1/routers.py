from fastapi import APIRouter

from api.v1.user import routers as user_router
from api.v1.product import routers as product_router
from api.v1.category import routers as category_router

router = APIRouter(prefix="/api/v1")

router.include_router(user_router.router)
router.include_router(product_router.router)
router.include_router(category_router.router)