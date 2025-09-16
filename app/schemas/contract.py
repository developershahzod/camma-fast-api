from datetime import datetime, date
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from .enums import ContractStatusEnum

class ContractBase(BaseModel):
    contract_number: str = Field(..., min_length=1, max_length=100)
    start_date: date
    end_date: date
    total_fights: int = Field(..., ge=1)
    base_fee: Optional[float] = Field(None, ge=0)
    win_bonus: Optional[float] = Field(None, ge=0)
    per_fight_bonus: Optional[float] = Field(None, ge=0)
    early_termination_penalty: Optional[float] = Field(None, ge=0)

class ContractCreate(ContractBase):
    fighter_id: int
    promotion_id: int
    contract_file_url: Optional[str] = None

class ContractResponse(ContractBase):
    id: int
    fighter_id: int
    promotion_id: int
    remaining_fights: int
    status: ContractStatusEnum
    verification_date: Optional[datetime] = None
    contract_file_url: Optional[str] = None
    created_at: datetime
    
    class Config:
        orm_mode = True

class ContractExtensionRequest(BaseModel):
    contract_id: int
    new_end_date: date
    additional_fights: int
    new_terms: Optional[Dict[str, Any]] = None

# Statistics models
class ContractStatsWidget(BaseModel):
    active_contracts: int
    expiring_contracts: int
    new_contracts_this_month: int
    new_contracts_last_month: int
    contract_dynamics: List[Dict[str, Any]]  # Monthly data