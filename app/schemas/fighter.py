from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, validator
from .enums import (
    GenderEnum, VerificationStatusEnum, ParticipationStatusEnum,
    ApplicationStatusEnum, UserRoleEnum
)

# Fighter models
class FighterBase(BaseModel):
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    birth_date: date
    birth_place: Optional[str] = Field(None, max_length=200)
    nationality: Optional[str] = Field(None, max_length=100)
    gender: GenderEnum
    height: Optional[int] = Field(None, ge=120, le=250)  # cm
    weight_class: Optional[str] = Field(None, max_length=50)
    wins: Optional[int] = Field(0, ge=0)
    losses: Optional[int] = Field(0, ge=0)
    draws: Optional[int] = Field(0, ge=0)

class FighterCreate(FighterBase):
    passport_series: Optional[str] = Field(None, max_length=10)
    passport_number: Optional[str] = Field(None, max_length=20)
    club_id: Optional[int] = None
    trainer_id: Optional[int] = None
    manager_id: Optional[int] = None
    promotion_id: Optional[int] = None

class FighterRegistrationByThirdParty(BaseModel):
    phone_number: str = Field(..., regex=r'^\+?[1-9]\d{1,14}$')
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)
    middle_name: Optional[str] = Field(None, max_length=100)
    passport_series: str = Field(..., max_length=10)
    passport_number: str = Field(..., max_length=20)
    birth_date: date
    gender: GenderEnum
    height: int = Field(..., ge=120, le=250)
    weight_class: str = Field(..., max_length=50)
    wins: int = Field(..., ge=0)
    losses: int = Field(..., ge=0)
    draws: int = Field(..., ge=0)
    club_id: Optional[int] = None
    trainer_id: Optional[int] = None
    manager_id: Optional[int] = None
    promotion_id: Optional[int] = None

    @validator('phone_number')
    def validate_phone(cls, v):
        if not v.startswith('+'):
            v = '+' + v
        return v

class FighterResponse(FighterBase):
    id: int
    fighter_id: str
    photo_url: Optional[str] = None
    last_fight_date: Optional[date] = None
    verification_status: VerificationStatusEnum
    participation_status: ParticipationStatusEnum
    is_verified: bool
    is_available: bool
    is_injured: bool
    injury_date: Optional[date] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class FighterProfile(FighterResponse):
    """Extended fighter profile with related data"""
    club: Optional[Dict[str, Any]] = None
    trainer: Optional[Dict[str, Any]] = None
    manager: Optional[Dict[str, Any]] = None
    promotion: Optional[Dict[str, Any]] = None
    active_contracts: List[Dict[str, Any]] = []
    recent_fights: List[Dict[str, Any]] = []
    achievements: List[Dict[str, Any]] = []

# Matchmaking models
class FighterCardForMatchmaking(BaseModel):
    id: int
    name: str
    weight_class: str
    age: int
    height: Optional[int] = None
    reach: Optional[int] = None
    total_fights: int
    recent_results: List[str]  # Last 3 fight results
    club: Optional[str] = None
    trainer: Optional[str] = None
    city: Optional[str] = None
    country: Optional[str] = None
    contract_expiry: Optional[date] = None
    remaining_fights: int
    application_status: ApplicationStatusEnum

class MatchSuggestion(BaseModel):
    opponent_id: int
    opponent_name: str
    compatibility_score: float
    reasons: List[str]  # Why this is a good match

# Response models for complex operations
class RegistrationResponse(BaseModel):
    success: bool
    message: str
    fighter_id: Optional[int] = None
    verification_required: bool = False