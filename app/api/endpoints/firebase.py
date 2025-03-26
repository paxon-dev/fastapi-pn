from fastapi import APIRouter, UploadFile, File, HTTPException
from app.config.settings import Settings
import json
import os

router = APIRouter()
settings = Settings()

@router.post("/upload-credentials")
async def upload_firebase_credentials(file: UploadFile = File(...)):
    """Upload Firebase credentials JSON file"""
    if not file.filename.endswith('.json'):
        raise HTTPException(status_code=400, detail="File must be a JSON file")

    try:
        # Read and validate JSON content
        content = await file.read()
        json_content = json.loads(content)

        # Check for required Firebase credential fields
        required_fields = ["type", "project_id", "private_key_id", "private_key"]
        for field in required_fields:
            if field not in json_content:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid Firebase credentials: missing {field}"
                )

        # Save file
        with open(settings.FIREBASE_CREDENTIALS_PATH, "wb") as f:
            f.write(content)

        return {
            "message": "Firebase credentials uploaded successfully",
            "path": settings.FIREBASE_CREDENTIALS_PATH
        }

    except json.JSONDecodeError:
        raise HTTPException(status_code=400, detail="Invalid JSON file")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/credentials-status")
async def check_credentials_status():
    """Check if Firebase credentials file exists"""
    exists = os.path.exists(settings.FIREBASE_CREDENTIALS_PATH)
    return {
        "exists": exists,
        "path": settings.FIREBASE_CREDENTIALS_PATH if exists else None
    }