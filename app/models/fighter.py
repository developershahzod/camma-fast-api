from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean, ForeignKey, Text, Float
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SQLEnum
from ..core.database import Base
from .enums import (
    GenderEnum, VerificationStatusEnum, ParticipationStatusEnum,
    ContractStatusEnum, EventTypeEnum, ApplicationStatusEnum,
    FightResultEnum, FightMethodEnum, TaskStatusEnum
)
from datetime import datetime

class Fighter(Base):
    __tablename__ = "fighters"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    fighter_id = Column(String(20), unique=True, index=True)  # Digital passport ID
    
    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    middle_name = Column(String(100))
    birth_date = Column(Date, nullable=False)
    birth_place = Column(String(200))
    nationality = Column(String(100))
    gender = Column(SQLEnum(GenderEnum), nullable=False)
    
    # Physical attributes
    height = Column(Integer)  # in cm
    weight_class = Column(String(50))
    
    # Passport data
    passport_series = Column(String(10))
    passport_number = Column(String(20))
    
    # Profile
    photo_url = Column(String(500))
    
    # Records
    wins = Column(Integer, default=0)
    losses = Column(Integer, default=0)
    draws = Column(Integer, default=0)
    last_fight_date = Column(Date)
    
    # Status
    verification_status = Column(SQLEnum(VerificationStatusEnum), default=VerificationStatusEnum.UNDER_REVIEW)
    participation_status = Column(SQLEnum(ParticipationStatusEnum), default=ParticipationStatusEnum.FREE_AGENT)
    is_verified = Column(Boolean, default=False)
    verification_date = Column(DateTime)
    verified_by = Column(String(100))
    
    # Flags
    is_available = Column(Boolean, default=True)
    is_injured = Column(Boolean, default=False)
    injury_date = Column(Date)
    
    # Relationships
    user = relationship("User", back_populates="fighter_profile")
    club_id = Column(Integer, ForeignKey("clubs.id"))
    trainer_id = Column(Integer, ForeignKey("trainers.id"))
    manager_id = Column(Integer, ForeignKey("managers.id"))
    promotion_id = Column(Integer, ForeignKey("promotions.id"))
    
    # Relationship objects
    club = relationship("Club", foreign_keys=[club_id])
    trainer = relationship("Trainer", foreign_keys=[trainer_id])
    manager = relationship("Manager", foreign_keys=[manager_id])
    promotion = relationship("Promotion", foreign_keys=[promotion_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Club(Base):
    __tablename__ = "clubs"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    address = Column(Text)
    city = Column(String(100))
    country = Column(String(100))
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Trainer(Base):
    __tablename__ = "trainers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    club_id = Column(Integer, ForeignKey("clubs.id"))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="trainer_profile")

class Manager(Base):
    __tablename__ = "managers"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    phone = Column(String(20))
    email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="manager_profile")

class Promotion(Base):
    __tablename__ = "promotions"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    description = Column(Text)
    website = Column(String(200))
    contact_email = Column(String(100))
    created_at = Column(DateTime, default=datetime.utcnow)

class Contract(Base):
    __tablename__ = "contracts"
    
    id = Column(Integer, primary_key=True, index=True)
    contract_number = Column(String(100), unique=True, nullable=False)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    promotion_id = Column(Integer, ForeignKey("promotions.id"), nullable=False)
    
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    total_fights = Column(Integer, nullable=False)
    remaining_fights = Column(Integer, nullable=False)
    
    # Contract terms
    base_fee = Column(Float)
    win_bonus = Column(Float)
    per_fight_bonus = Column(Float)
    early_termination_penalty = Column(Float)
    
    status = Column(SQLEnum(ContractStatusEnum), default=ContractStatusEnum.UNDER_REVIEW)
    verification_date = Column(DateTime)
    contract_file_url = Column(String(500))
    
    # Relationships
    fighter = relationship("Fighter", foreign_keys=[fighter_id])
    promotion = relationship("Promotion", foreign_keys=[promotion_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Event(Base):
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    event_type = Column(SQLEnum(EventTypeEnum), nullable=False)
    event_date = Column(DateTime, nullable=False)
    venue = Column(String(200))
    city = Column(String(100))
    country = Column(String(100))
    organizer_id = Column(Integer, ForeignKey("promotions.id"))
    
    total_slots = Column(Integer, default=0)
    confirmed_pairs = Column(Integer, default=0)
    pending_applications = Column(Integer, default=0)
    approved_without_pair = Column(Integer, default=0)
    
    poster_url = Column(String(500))
    description = Column(Text)
    
    # Relationships
    organizer = relationship("Promotion", foreign_keys=[organizer_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class EventApplication(Base):
    __tablename__ = "event_applications"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    applicant_user_id = Column(Integer, ForeignKey("users.id"), nullable=False)  # Who submitted
    
    desired_weight_class = Column(String(50))
    comments = Column(Text)
    status = Column(SQLEnum(ApplicationStatusEnum), default=ApplicationStatusEnum.DRAFT)
    
    # Medical documents
    medical_docs_url = Column(String(500))
    antidoping_test_date = Column(Date)
    antidoping_test_result = Column(String(100))
    antidoping_conducted_by = Column(String(200))
    
    # Relationships
    event = relationship("Event", foreign_keys=[event_id])
    fighter = relationship("Fighter", foreign_keys=[fighter_id])
    applicant = relationship("User", foreign_keys=[applicant_user_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Fight(Base):
    __tablename__ = "fights"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    fighter1_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    fighter2_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    
    fight_number = Column(Integer)  # Fight order in event
    weight_class = Column(String(50))
    rounds = Column(Integer, default=3)
    round_duration = Column(Integer, default=5)  # minutes
    
    # Results
    winner_id = Column(Integer, ForeignKey("fighters.id"))
    result = Column(SQLEnum(FightResultEnum))
    method = Column(SQLEnum(FightMethodEnum))
    round_ended = Column(Integer)
    time_ended = Column(String(10))  # MM:SS format
    
    # Media
    video_url = Column(String(500))
    highlight_url = Column(String(500))
    
    # Relationships
    event = relationship("Event", foreign_keys=[event_id])
    fighter1 = relationship("Fighter", foreign_keys=[fighter1_id])
    fighter2 = relationship("Fighter", foreign_keys=[fighter2_id])
    winner = relationship("Fighter", foreign_keys=[winner_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Achievement(Base):
    __tablename__ = "achievements"
    
    id = Column(Integer, primary_key=True, index=True)
    fighter_id = Column(Integer, ForeignKey("fighters.id"), nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    date_achieved = Column(Date)
    certificate_url = Column(String(500))
    
    # Relationships
    fighter = relationship("Fighter", foreign_keys=[fighter_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)

class Task(Base):
    __tablename__ = "tasks"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)
    status = Column(SQLEnum(TaskStatusEnum), default=TaskStatusEnum.TODO)
    priority = Column(String(20), default="medium")  # low, medium, high
    
    assigned_to_id = Column(Integer, ForeignKey("users.id"))
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    due_date = Column(DateTime)
    completed_date = Column(DateTime)
    
    # Event relation for event-specific tasks
    event_id = Column(Integer, ForeignKey("events.id"))
    
    # Checklist items (JSON)
    checklist_items = Column(Text)  # JSON string of checklist items
    
    # Relationships
    assigned_to = relationship("User", foreign_keys=[assigned_to_id])
    created_by = relationship("User", foreign_keys=[created_by_id])
    event = relationship("Event", foreign_keys=[event_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class MediaContent(Base):
    __tablename__ = "media_content"
    
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(Integer, ForeignKey("events.id"), nullable=False)
    title = Column(String(200), nullable=False)
    file_url = Column(String(500), nullable=False)
    file_type = Column(String(50))  # image, video, document
    tags = Column(Text)  # JSON array of tags
    description = Column(Text)
    
    uploaded_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    event = relationship("Event", foreign_keys=[event_id])
    uploaded_by = relationship("User", foreign_keys=[uploaded_by_id])
    
    created_at = Column(DateTime, default=datetime.utcnow)