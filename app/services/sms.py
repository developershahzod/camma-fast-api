import httpx
from ..core.config import settings

async def send_sms(phone_number: str, message: str) -> bool:
    """Send SMS using external service"""
    
    if not settings.SMS_API_KEY:
        print(f"SMS to {phone_number}: {message}")  # Development mode
        return True
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(
                settings.SMS_API_URL,
                headers={"Authorization": f"Bearer {settings.SMS_API_KEY}"},
                json={
                    "to": phone_number,
                    "message": message
                }
            )
            return response.status_code == 200
        except Exception as e:
            print(f"SMS sending failed: {e}")
            return False