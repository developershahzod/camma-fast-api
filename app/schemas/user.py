from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, EmailStr, validator, ConfigDict
from .enums import UserRoleEnum

class UserBase(BaseModel):
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$') 
    email: Optional[EmailStr] = None
    role: UserRoleEnum

class UserCreate(UserBase):
    password: Optional[str] = None

class UserLogin(BaseModel):
    phone_number: str
    otp_code: str

class UserResponse(UserBase):
    id: int
    is_active: bool
    created_at: Optional[str] = None
    
    # This is the problem - you have both Config class AND model_config
    model_config = ConfigDict(from_attributes=True)
    
    class Config:  # ← This needs to be removed completely
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class OTPRequest(BaseModel):
    phone_number: str = Field(..., pattern=r'^\+?[1-9]\d{1,14}$')

class OTPResponse(BaseModel):
    message: str
    expires_in: int

# Validation functions
@validator('phone_number')
def validate_phone(cls, v):
    if not v.startswith('+'):
        v = '+' + v
    return v