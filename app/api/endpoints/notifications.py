from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from app.services.fcm_service import FCMService
from firebase_admin import messaging

router = APIRouter()

class NotificationBase(BaseModel):
    title: str = Field(..., description="Notification title")
    body: str = Field(..., description="Notification body")
    data: Optional[Dict] = Field(default=None, description="Additional data payload")

class SingleNotificationRequest(NotificationBase):
    token: str = Field(..., description="FCM device token")

class MulticastNotificationRequest(NotificationBase):
    tokens: List[str] = Field(..., min_items=1, max_items=500, description="List of FCM device tokens")

@router.post("/send",
    summary="Send notification to a single device",
    response_description="Message ID if successful")
async def send_notification(request: SingleNotificationRequest):
    """
    Send a push notification to a single device using FCM.

    - **token**: FCM device token
    - **title**: Notification title
    - **body**: Notification body
    - **data**: Optional additional data payload
    """
    try:
        result = await FCMService.send_message(
            token=request.token,
            title=request.title,
            body=request.body,
            data=request.data
        )
        return {"message_id": result, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-multicast",
    summary="Send notification to multiple devices",
    response_description="Multicast message results")
async def send_multicast_notification(request: MulticastNotificationRequest):
    """
    Send a push notification to multiple devices using FCM.

    - **tokens**: List of FCM device tokens (max 500)
    - **title**: Notification title
    - **body**: Notification body
    - **data**: Optional additional data payload
    """
    try:
        result = await FCMService.send_multicast(
            tokens=request.tokens,
            title=request.title,
            body=request.body,
            data=request.data
        )

        return {
            "success_count": result.success_count,
            "failure_count": result.failure_count,
            "responses": [
                {
                    "success": resp.success,
                    "message_id": resp.message_id,
                    "exception": str(resp.exception) if resp.exception else None
                }
                for resp in result.responses
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/send-topic",
    summary="Send notification to a topic",
    response_description="Message ID if successful")
async def send_topic_notification(
    topic: str,
    notification: NotificationBase
):
    """
    Send a push notification to all devices subscribed to a specific topic.

    - **topic**: Topic name
    - **title**: Notification title
    - **body**: Notification body
    - **data**: Optional additional data payload
    """
    try:
        # Remove any leading '/' from the topic name
        topic = topic.lstrip('/')

        message = messaging.Message(
            notification=messaging.Notification(
                title=notification.title,
                body=notification.body
            ),
            data=notification.data,
            topic=topic,
        )

        result = messaging.send(message)
        return {"message_id": result, "success": True}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
