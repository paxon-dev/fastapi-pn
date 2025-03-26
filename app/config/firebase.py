import firebase_admin
from firebase_admin import credentials, messaging
from app.config.settings import Settings
import os

settings = Settings()
_firebase_app = None

def initialize_firebase():
    """Initialize Firebase Admin SDK"""
    global _firebase_app
    if _firebase_app is not None:
        return _firebase_app

    if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
        return None

    try:
        cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
        _firebase_app = firebase_admin.initialize_app(cred)
        return _firebase_app
    except Exception as e:
        print(f"Failed to initialize Firebase: {str(e)}")
        return None
    finally:
        print(f"--- Firebase initialization complete:")
        print(f"  - App Name: {_firebase_app.name}")
        print(f"  - Project ID: {_firebase_app.project_id}")
        # print(f"  - Full Details: {_firebase_app.__dict__}")
        # print(f"  - Credentials: {_firebase_app._credential.__dict__}")
        # print(f"  - Options: {_firebase_app._options.__dict__}")

def get_firebase_app():
    """Get Firebase app instance, initialize if needed"""
    global _firebase_app
    if _firebase_app is None:
        _firebase_app = initialize_firebase()
    return _firebase_app
