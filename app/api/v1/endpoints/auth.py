import random
from datetime import datetime, timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.security import create_access_token, get_password_hash
from ....models.user import User
from ....schemas.user import OTPRequest, OTPResponse, UserLogin, Token, UserResponse
from ....schemas.enums import UserRoleEnum

router = APIRouter()

def generate_otp() -> str:
    """Generate a 6-digit OTP code"""
    return f"{random.randint(100000, 999999)}"

def send_otp(phone_number: str, otp_code: str) -> bool:
    """Send OTP via SMS - implement with your SMS provider"""
    print(f"Sending OTP {otp_code} to {phone_number}")  # For development
    return True

@router.post("/request-otp", response_model=OTPResponse)
def request_otp(
    request: OTPRequest,
    db: Session = Depends(get_db)
) -> Any:
    """Request OTP for phone number"""
    
    # Generate OTP
    otp_code = generate_otp()
    expires_at = datetime.utcnow() + timedelta(minutes=5)  # 5 minutes expiry
    
    # Find or create user
    user = db.query(User).filter(User.phone_number == request.phone_number).first()
    if not user:
        user = User(
            phone_number=request.phone_number,
            role=UserRoleEnum.FIGHTER,  # Default role
            otp_code=otp_code,
            otp_expires_at=expires_at
        )
        db.add(user)
    else:
        user.otp_code = otp_code
        user.otp_expires_at = expires_at
    
    db.commit()
    
    # Send OTP (implement with SMS service)
    if not send_otp(request.phone_number, otp_code):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to send OTP"
        )
    
    return OTPResponse(
        message="OTP sent successfully",
        expires_in=300  # 5 minutes
    )

@router.post("/login", response_model=Token)
def login(
    user_credentials: UserLogin,
    db: Session = Depends(get_db)
) -> Any:
    """Login with phone number and OTP"""
    
    user = db.query(User).filter(
        User.phone_number == user_credentials.phone_number
    ).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    
    # Check OTP
    if (not user.otp_code or 
        user.otp_code != user_credentials.otp_code or
        user.otp_expires_at < datetime.utcnow()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired OTP"
        )
    
    # Clear OTP after successful login
    user.otp_code = None
    user.otp_expires_at = None
    user.is_verified = True
    db.commit()
    
    # Create access token
    access_token = create_access_token(subject=user.id)
    
    return Token(access_token=access_token, token_type="bearer")