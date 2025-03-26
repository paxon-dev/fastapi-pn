from fastapi import APIRouter

from app.api.endpoints import apis, firebase


api_router = APIRouter(prefix="/api")


api_router.include_router(apis.router, prefix="", tags=["Public"])
api_router.include_router(firebase.router, prefix="/firebase", tags=["Firebase"])
