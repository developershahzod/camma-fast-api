from datetime import datetime, date
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from .enums import EventTypeEnum, ApplicationStatusEnum, FightResultEnum, FightMethodEnum

# Event models
class EventBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    event_type: EventTypeEnum
    event_date: datetime
    venue: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    country: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None

class EventCreate(EventBase):
    organizer_id: int
    total_slots: Optional[int] = Field(0, ge=0)

class EventResponse(EventBase):
    id: int
    organizer_id: int
    total_slots: int
    confirmed_pairs: int
    pending_applications: int
    approved_without_pair: int
    poster_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

# Event Application models
class EventApplicationBase(BaseModel):
    desired_weight_class: Optional[str] = Field(None, max_length=50)
    comments: Optional[str] = None

class EventApplicationCreate(EventApplicationBase):
    event_id: int
    fighter_id: int

class EventApplicationResponse(EventApplicationBase):
    id: int
    event_id: int
    fighter_id: int
    applicant_user_id: int
    status: ApplicationStatusEnum
    medical_docs_url: Optional[str] = None
    antidoping_test_date: Optional[date] = None
    antidoping_test_result: Optional[str] = None
    antidoping_conducted_by: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

# Fight models
class FightBase(BaseModel):
    fight_number: Optional[int] = Field(None, ge=1)
    weight_class: Optional[str] = Field(None, max_length=50)
    rounds: Optional[int] = Field(3, ge=1, le=5)
    round_duration: Optional[int] = Field(5, ge=3, le=10)

class FightCreate(FightBase):
    event_id: int
    fighter1_id: int
    fighter2_id: int

class FightResult(BaseModel):
    winner_id: Optional[int] = None
    result: Optional[FightResultEnum] = None
    method: Optional[FightMethodEnum] = None
    round_ended: Optional[int] = Field(None, ge=1)
    time_ended: Optional[str] = Field(None, regex=r'^\d{1,2}:\d{2}$')
    video_url: Optional[str] = None
    highlight_url: Optional[str] = None

class FightResponse(FightBase, FightResult):
    id: int
    event_id: int
    fighter1_id: int
    fighter2_id: int
    created_at: datetime
    
    class Config:
        orm_mode = True

class CreateFightPair(BaseModel):
    fighter1_id: int
    fighter2_id: int
    weight_class: str
    rounds: int = 3
    round_duration: int = 5
    fight_number: Optional[int] = None

class EventParticipationInvite(BaseModel):
    fighter_id: int
    event_id: int
    potential_opponents: List[int]
    deadline: datetime
    personal_message: Optional[str] = None

# Statistics models
class ApplicationStatsWidget(BaseModel):
    draft: int
    submitted: int
    under_review: int
    approved: int
    waiting_list: int
    rejected: int
    confirmed: int
    blocked: int
    completed: int

class MatchmakingStats(BaseModel):
    total_events: int
    pending_applications: int
    approved_pairs: int
    approved_without_pair: int
    applications_by_status: ApplicationStatsWidget