from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config.settings import Settings
from app.api.api import api_router
from app.config.firebase import initialize_firebase

settings = Settings()

# Create FastAPI app
app = FastAPI(title=settings.APP_NAME)

# Try to initialize Firebase (but don't fail if credentials aren't present)
initialize_firebase()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
