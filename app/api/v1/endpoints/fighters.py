from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....models.fighter import Fighter, Club, Trainer, Manager, Promotion
from ....schemas.fighter import FighterCreate, FighterResponse, FighterRegistrationByThirdParty, RegistrationResponse
import uuid

router = APIRouter()

@router.post("/", response_model=FighterResponse)
def create_fighter(
    fighter: FighterCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create new fighter"""
    
    # Generate unique fighter ID
    fighter_id = f"CAMMA{uuid.uuid4().hex[:8].upper()}"
    
    db_fighter = Fighter(
        user_id=current_user.id,
        fighter_id=fighter_id,
        **fighter.dict()
    )
    db.add(db_fighter)
    db.commit()
    db.refresh(db_fighter)
    return db_fighter

@router.get("/", response_model=List[FighterResponse])
def read_fighters(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve fighters"""
    fighters = db.query(Fighter).offset(skip).limit(limit).all()
    return fighters

@router.get("/{fighter_id}", response_model=FighterResponse)
def read_fighter(
    fighter_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get fighter by ID"""
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()
    if fighter is None:
        raise HTTPException(status_code=404, detail="Fighter not found")
    return fighter

@router.post("/{fighter_id}/upload-photo")
async def upload_fighter_photo(
    fighter_id: int,
    photo: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Upload fighter photo"""
    
    fighter = db.query(Fighter).filter(Fighter.id == fighter_id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    
    # Save file (implement file storage logic)
    file_path = f"uploads/fighters/{fighter_id}_{photo.filename}"
    # with open(file_path, "wb") as buffer:
    #     content = await photo.read()
    #     buffer.write(content)
    
    fighter.photo_url = file_path
    db.commit()
    
    return {"message": "Photo uploaded successfully", "photo_url": file_path}

@router.post("/register-by-third-party", response_model=RegistrationResponse)
def register_fighter_by_third_party(
    registration: FighterRegistrationByThirdParty,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Register fighter by third party (trainer, manager, etc.)"""
    
    # Check if user with phone number already exists
    existing_user = db.query(User).filter(User.phone_number == registration.phone_number).first()
    
    if existing_user:
        # Check if user already has a fighter profile
        existing_fighter = db.query(Fighter).filter(Fighter.user_id == existing_user.id).first()
        if existing_fighter:
            return RegistrationResponse(
                success=False,
                message="Fighter with this phone number already exists",
                verification_required=False
            )
    else:
        # Create new user
        from ....schemas.enums import UserRoleEnum
        new_user = User(
            phone_number=registration.phone_number,
            role=UserRoleEnum.FIGHTER,
            is_active=True,
            is_verified=False
        )
        db.add(new_user)
        db.flush()  # Get the ID
        existing_user = new_user
    
    # Generate unique fighter ID
    fighter_id = f"CAMMA{uuid.uuid4().hex[:8].upper()}"
    
    # Create fighter profile
    fighter_data = registration.dict()
    fighter_data.pop('phone_number')  # Remove phone_number as it's not part of Fighter model
    
    db_fighter = Fighter(
        user_id=existing_user.id,
        fighter_id=fighter_id,
        **fighter_data
    )
    db.add(db_fighter)
    db.commit()
    db.refresh(db_fighter)
    
    return RegistrationResponse(
        success=True,
        message="Fighter registered successfully",
        fighter_id=db_fighter.id,
        verification_required=True
    )