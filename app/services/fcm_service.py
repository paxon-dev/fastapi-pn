from firebase_admin import messaging, credentials
from firebase_admin.exceptions import FirebaseError
from typing import List, Dict, Optional
from fastapi import HTTPException
from app.config.firebase import get_firebase_app, initialize_firebase
from app.config.settings import Settings
import os
import time

settings = Settings()

class FCMService:
    @staticmethod
    async def _check_firebase():
        """Enhanced Firebase check with detailed diagnostics"""
        app = get_firebase_app()
        if app is None:
            # Try to reinitialize
            print("Firebase app not found, attempting to reinitialize...")
            app = initialize_firebase()

            if app is None:
                # Check credentials file
                if not os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                    print(f"Firebase credentials file not found at: {settings.FIREBASE_CREDENTIALS_PATH}")
                    raise HTTPException(
                        status_code=503,
                        detail="Firebase credentials file not found. Please upload credentials first."
                    )

                # Try to read and validate credentials
                try:
                    cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                    print(f"Loaded credentials for project: {cred.project_id}")
                except Exception as e:
                    print(f"Failed to load Firebase credentials: {str(e)}")
                    raise HTTPException(
                        status_code=503,
                        detail="Invalid Firebase credentials. Please check the credentials file."
                    )

                raise HTTPException(
                    status_code=503,
                    detail="Firebase initialization failed. Please check server logs."
                )

    @staticmethod
    async def _validate_token(token: str):
        if not isinstance(token, str) or not token.strip():
            raise HTTPException(
                status_code=400,
                detail="Invalid FCM token"
            )

    @staticmethod
    async def _validate_data(data: Optional[Dict]):
        if data is not None:
            if not isinstance(data, dict):
                raise HTTPException(
                    status_code=400,
                    detail="Data payload must be a dictionary"
                )
            # Convert all values to strings as required by FCM
            return {k: str(v) for k, v in data.items()}
        return None

    @staticmethod
    async def send_message(
        token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ):
        """Send FCM notification to a single device with enhanced error handling"""
        try:
            await FCMService._check_firebase()
            await FCMService._validate_token(token)
            validated_data = await FCMService._validate_data(data)

            print(f"--- Preparing FCM message for token: {token[:10]}...")
            message = messaging.Message(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=validated_data,
                token=token,
            )
            print(f"--- Sending FCM message to token: {token[:10]}...")

            try:
                print(f"Attempting to send FCM message to token: {token[:10]}...")
                result = messaging.send(message)
                print(f"Successfully sent message: {result}")
                return result
            except FirebaseError as firebase_error:
                error_message = str(firebase_error)
                error_dict = getattr(firebase_error, '__dict__', {})
                print(f"Firebase error: {error_message}")
                print(f"Error details: {error_dict}")

                # Get HTTP response if available
                http_response = error_dict.get('_http_response')
                if http_response:
                    print(f"HTTP Status: {http_response.status_code}")
                    print(f"Response body: {http_response.text}")

                if 'auth-error' in error_message.lower() or 'unauthenticated' in str(error_dict).lower():
                    # Check credentials file age
                    creds_path = settings.FIREBASE_CREDENTIALS_PATH
                    if os.path.exists(creds_path):
                        creds_age = time.time() - os.path.getmtime(creds_path)
                        print(f"Credentials file age: {creds_age/86400:.1f} days")

                    raise HTTPException(
                        status_code=500,
                        detail=(
                            "Firebase authentication failed. Please ensure:\n"
                            "1. Your credentials file is valid and not expired\n"
                            "2. The service account has the necessary permissions\n"
                            "3. The project is active and billing is enabled\n"
                            "4. Cloud Messaging API is enabled in Google Cloud Console"
                        )
                    )
                elif 'invalid-argument' in error_message:
                    raise HTTPException(
                        status_code=400,
                        detail="Invalid FCM token format"
                    )
                elif 'registration-token-not-registered' in error_message:
                    raise HTTPException(
                        status_code=400,
                        detail="FCM token is no longer valid"
                    )
                else:
                    raise HTTPException(
                        status_code=500,
                        detail=f"Firebase error: {error_message}"
                    )

        except HTTPException:
            raise
        except Exception as e:
            print(f"Unexpected error while sending notification: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send notification: {str(e)}"
            )

    @staticmethod
    async def send_multicast(
        tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None
    ):
        """Send FCM notification to multiple devices"""
        try:
            await FCMService._check_firebase()
            for token in tokens:
                await FCMService._validate_token(token)
            validated_data = await FCMService._validate_data(data)

            message = messaging.MulticastMessage(
                notification=messaging.Notification(
                    title=title,
                    body=body
                ),
                data=validated_data,
                tokens=tokens,
            )

            try:
                return messaging.send_multicast(message)
            except FirebaseError as firebase_error:
                raise HTTPException(
                    status_code=500,
                    detail=f"Firebase error: {str(firebase_error)}"
                )

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to send multicast notification: {str(e)}"
            )
