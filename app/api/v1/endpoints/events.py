from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....models.fighter import Event, EventApplication, Fight, Fighter
from ....schemas.event import (
    EventCreate, EventResponse, EventApplicationCreate, 
    EventApplicationResponse, FightCreate, FightResponse,
    CreateFightPair
)

router = APIRouter()

@router.post("/", response_model=EventResponse)
def create_event(
    event: EventCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create new event"""
    
    db_event = Event(**event.dict())
    db.add(db_event)
    db.commit()
    db.refresh(db_event)
    return db_event

@router.get("/", response_model=List[EventResponse])
def read_events(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve events"""
    events = db.query(Event).offset(skip).limit(limit).all()
    return events

@router.get("/{event_id}", response_model=EventResponse)
def read_event(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get event by ID"""
    event = db.query(Event).filter(Event.id == event_id).first()
    if event is None:
        raise HTTPException(status_code=404, detail="Event not found")
    return event

@router.post("/{event_id}/applications", response_model=EventApplicationResponse)
def create_event_application(
    event_id: int,
    application: EventApplicationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create event application"""
    
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Verify fighter exists
    fighter = db.query(Fighter).filter(Fighter.id == application.fighter_id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    
    db_application = EventApplication(
        event_id=event_id,
        applicant_user_id=current_user.id,
        **application.dict()
    )
    db.add(db_application)
    db.commit()
    db.refresh(db_application)
    return db_application

@router.get("/{event_id}/applications", response_model=List[EventApplicationResponse])
def read_event_applications(
    event_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get applications for event"""
    applications = db.query(EventApplication).filter(
        EventApplication.event_id == event_id
    ).all()
    return applications

@router.post("/{event_id}/fights", response_model=FightResponse)
def create_fight(
    event_id: int,
    fight: FightCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create fight for event"""
    
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Verify fighters exist
    fighter1 = db.query(Fighter).filter(Fighter.id == fight.fighter1_id).first()
    fighter2 = db.query(Fighter).filter(Fighter.id == fight.fighter2_id).first()
    
    if not fighter1 or not fighter2:
        raise HTTPException(status_code=404, detail="One or both fighters not found")
    
    if fighter1.id == fighter2.id:
        raise HTTPException(status_code=400, detail="Fighter cannot fight themselves")
    
    db_fight = Fight(
        event_id=event_id,
        **fight.dict()
    )
    db.add(db_fight)
    db.commit()
    db.refresh(db_fight)
    return db_fight

@router.post("/{event_id}/create-pair")
def create_fight_pair(
    event_id: int,
    pair: CreateFightPair,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create a fight pair for matchmaking"""
    
    # Verify event exists
    event = db.query(Event).filter(Event.id == event_id).first()
    if not event:
        raise HTTPException(status_code=404, detail="Event not found")
    
    # Create the fight
    db_fight = Fight(
        event_id=event_id,
        fighter1_id=pair.fighter1_id,
        fighter2_id=pair.fighter2_id,
        weight_class=pair.weight_class,
        rounds=pair.rounds,
        round_duration=pair.round_duration,
        fight_number=pair.fight_number
    )
    db.add(db_fight)
    
    # Update event statistics
    event.confirmed_pairs += 1
    
    db.commit()
    db.refresh(db_fight)
    
    return {"message": "Fight pair created successfully", "fight_id": db_fight.id}