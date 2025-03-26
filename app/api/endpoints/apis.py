from fastapi import APIRouter


router = APIRouter()

@router.get("/", name="Root")
async def read_root():
    return {"message": "ok"}