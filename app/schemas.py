from pydantic import BaseModel, Field
from typing import Optional
from uuid import UUID  
from app.models import TaskStatus

class UserCreate(BaseModel):
    first_name: str
    last_name: Optional[str] = None
    username: str
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    first_name: str
    last_name: Optional[str]
    username: str

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.new

class TaskOut(TaskCreate):
    id: UUID  
    user_id: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None
