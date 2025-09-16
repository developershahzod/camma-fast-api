from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from ....core.database import get_db
from ....core.deps import get_current_active_user
from ....models.user import User
from ....models.fighter import Task
from ....schemas.task import TaskCreate, TaskResponse, TaskUpdate
import json

router = APIRouter()

@router.post("/", response_model=TaskResponse)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Create new task"""
    
    task_data = task.dict()
    if task_data.get('checklist_items'):
        task_data['checklist_items'] = json.dumps(task_data['checklist_items'])
    
    db_task = Task(
        created_by_id=current_user.id,
        **task_data
    )
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    
    # Parse checklist items back to list for response
    if db_task.checklist_items:
        db_task.checklist_items = json.loads(db_task.checklist_items)
    
    return db_task

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    assigned_to_me: bool = False,
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Retrieve tasks"""
    query = db.query(Task)
    
    if assigned_to_me:
        query = query.filter(Task.assigned_to_id == current_user.id)
    
    tasks = query.offset(skip).limit(limit).all()
    
    # Parse checklist items for each task
    for task in tasks:
        if task.checklist_items:
            task.checklist_items = json.loads(task.checklist_items)
    
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Get task by ID"""
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Parse checklist items
    if task.checklist_items:
        task.checklist_items = json.loads(task.checklist_items)
    
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Update task"""
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_update.dict(exclude_unset=True)
    
    # Handle checklist items
    if 'checklist_items' in update_data and update_data['checklist_items']:
        update_data['checklist_items'] = json.dumps(update_data['checklist_items'])
    
    for field, value in update_data.items():
        setattr(task, field, value)
    
    db.commit()
    db.refresh(task)
    
    # Parse checklist items back to list for response
    if task.checklist_items:
        task.checklist_items = json.loads(task.checklist_items)
    
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """Delete task"""
    
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    
    # Check if user can delete (creator or assigned user)
    if task.created_by_id != current_user.id and task.assigned_to_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")
    
    db.delete(task)
    db.commit()
    
    return {"message": "Task deleted successfully"}