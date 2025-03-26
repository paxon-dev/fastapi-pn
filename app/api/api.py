from fastapi import APIRouter

from app.api.endpoints import apis


api_router = APIRouter(prefix="/api/v1")


api_router.include_router(apis.router, prefix="", tags=["Public"])