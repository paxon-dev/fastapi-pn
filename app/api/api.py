from fastapi import APIRouter

from app.api.endpoints import apis, firebase, notifications


api_router = APIRouter(prefix="/api")


api_router.include_router(apis.router, prefix="", tags=["Public"])
api_router.include_router(firebase.router, prefix="/firebase", tags=["Firebase"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["Notifications"])
