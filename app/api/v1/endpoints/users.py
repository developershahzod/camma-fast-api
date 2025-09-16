from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....schemas.user import UserResponse

router = APIRouter()

@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get current user"""
    return current_user

@router.get("/", response_model=List[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve users"""
    users = db.query(User).offset(skip).limit(limit).all()
    return users