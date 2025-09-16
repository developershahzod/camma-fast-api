from typing import Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....models.fighter import Fighter

router = APIRouter()

@router.get("/stats")
def get_dashboard_stats(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get dashboard statistics"""
    
    total_fighters = db.query(Fighter).count()
    verified_fighters = db.query(Fighter).filter(Fighter.is_verified == True).count()
    active_fighters = db.query(Fighter).filter(Fighter.is_available == True).count()
    
    return {
        "total_fighters": total_fighters,
        "verified_fighters": verified_fighters,
        "active_fighters": active_fighters,
        "verification_rate": (verified_fighters / total_fighters * 100) if total_fighters > 0 else 0
    }