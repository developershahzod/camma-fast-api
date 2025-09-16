from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field
from .enums import TaskStatusEnum

class TaskBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field("medium", regex=r'^(low|medium|high)$')
    due_date: Optional[datetime] = None

class TaskCreate(TaskBase):
    assigned_to_id: Optional[int] = None
    event_id: Optional[int] = None
    checklist_items: Optional[List[str]] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = None
    status: Optional[TaskStatusEnum] = None
    priority: Optional[str] = Field(None, regex=r'^(low|medium|high)$')
    assigned_to_id: Optional[int] = None
    due_date: Optional[datetime] = None
    checklist_items: Optional[List[str]] = None

class TaskResponse(TaskBase):
    id: int
    status: TaskStatusEnum
    assigned_to_id: Optional[int] = None
    created_by_id: int
    event_id: Optional[int] = None
    completed_date: Optional[datetime] = None
    checklist_items: Optional[List[str]] = None
    created_at: datetime
    
    class Config:
        orm_mode = True