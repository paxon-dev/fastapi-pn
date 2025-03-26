from firebase_admin import messaging
from typing import List, Dict, Optional
from fastapi import HTTPException
from app.config.firebase import get_firebase_app

class FCMService:
    @staticmethod
    async def _check_firebase():
        if get_firebase_app() is None:
            raise HTTPException(
                status_code=503,
                detail="Firebase service is not initialized. Please upload credentials first."
            )

    @staticmethod
    async def send_message(
        token: str,
        title: str,
        body: str,
        data: Optional[Dict] = None
    ):
        """Send FCM notification to a single device"""
        await FCMService._check_firebase()

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data,
            token=token,
        )

        return messaging.send(message)

    @staticmethod
    async def send_multicast(
        tokens: List[str],
        title: str,
        body: str,
        data: Optional[Dict] = None
    ):
        """Send FCM notification to multiple devices"""
        await FCMService._check_firebase()

        message = messaging.MulticastMessage(
            notification=messaging.Notification(
                title=title,
                body=body
            ),
            data=data,
            tokens=tokens,
        )

        return messaging.send_multicast(message)
