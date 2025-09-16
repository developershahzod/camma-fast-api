from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....models.fighter import Contract, Fighter, Promotion
from ....schemas.contract import ContractCreate, ContractResponse, ContractExtensionRequest
import uuid

router = APIRouter()

@router.post("/", response_model=ContractResponse)
def create_contract(
    contract: ContractCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create new contract"""
    
    # Verify fighter exists
    fighter = db.query(Fighter).filter(Fighter.id == contract.fighter_id).first()
    if not fighter:
        raise HTTPException(status_code=404, detail="Fighter not found")
    
    # Verify promotion exists
    promotion = db.query(Promotion).filter(Promotion.id == contract.promotion_id).first()
    if not promotion:
        raise HTTPException(status_code=404, detail="Promotion not found")
    
    db_contract = Contract(
        **contract.dict(),
        remaining_fights=contract.total_fights
    )
    db.add(db_contract)
    db.commit()
    db.refresh(db_contract)
    return db_contract

@router.get("/", response_model=List[ContractResponse])
def read_contracts(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve contracts"""
    contracts = db.query(Contract).offset(skip).limit(limit).all()
    return contracts

@router.get("/{contract_id}", response_model=ContractResponse)
def read_contract(
    contract_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get contract by ID"""
    contract = db.query(Contract).filter(Contract.id == contract_id).first()
    if contract is None:
        raise HTTPException(status_code=404, detail="Contract not found")
    return contract

@router.post("/extend")
def extend_contract(
    extension: ContractExtensionRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Extend existing contract"""
    
    contract = db.query(Contract).filter(Contract.id == extension.contract_id).first()
    if not contract:
        raise HTTPException(status_code=404, detail="Contract not found")
    
    contract.end_date = extension.new_end_date
    contract.total_fights += extension.additional_fights
    contract.remaining_fights += extension.additional_fights
    
    db.commit()
    
    return {"message": "Contract extended successfully", "contract_id": contract.id}