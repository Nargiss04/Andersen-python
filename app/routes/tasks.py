from fastapi import APIRouter, Depends, HTTPException
from typing import List, Optional
from uuid import uuid4, UUID
from app.schemas import TaskCreate, TaskOut, TaskUpdate
from app.models import tasks, TaskStatus
from app.database import database
from app.auth import get_current_user

router = APIRouter()

MAX_LIMIT = 50

@router.post("/tasks", response_model=TaskOut)
async def create_task(task: TaskCreate, user=Depends(get_current_user)):
    task_id = uuid4()
    query = tasks.insert().values(
        id=task_id,
        title=task.title,
        description=task.description,
        status=task.status,
        user_id=user["username"]
    )
    await database.execute(query)
    return {**task.dict(), "id": str(task_id), "user_id": user["username"]}

@router.get("/tasks", response_model=List[TaskOut])
async def get_tasks(limit: int = 10, offset: int = 0, user=Depends(get_current_user)):
    query = tasks.select().offset(offset).limit(min(limit, MAX_LIMIT))
    return await database.fetch_all(query)

@router.get("/tasks/user", response_model=List[TaskOut])
async def get_user_tasks(limit: int = 10, offset: int = 0, user=Depends(get_current_user)):
    query = tasks.select().where(tasks.c.user_id == user["username"]).offset(offset).limit(min(limit, MAX_LIMIT))
    return await database.fetch_all(query)

# IMPORTANT: define static route before dynamic route
@router.get("/tasks/filter", response_model=List[TaskOut])
async def filter_tasks_by_status(status: TaskStatus, user=Depends(get_current_user)):
    query = tasks.select().where(tasks.c.status == status).where(tasks.c.user_id == user["username"])
    return await database.fetch_all(query)

@router.get("/tasks/{task_id}", response_model=TaskOut)
async def get_task(task_id: UUID, user=Depends(get_current_user)):
    task = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))
    if not task or task["user_id"] != user["username"]:
        raise HTTPException(status_code=404, detail="Not found")
    return task

@router.put("/tasks/{task_id}", response_model=TaskOut)
async def update_task(task_id: UUID, update: TaskUpdate, user=Depends(get_current_user)):
    existing = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))
    if not existing:
        raise HTTPException(status_code=404, detail="Task not found")
    if existing["user_id"] != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    update_data = update.dict(exclude_unset=True)
    query = tasks.update().where(tasks.c.id == task_id).values(**update_data)
    await database.execute(query)
    return {**existing, **update_data}

@router.delete("/tasks/{task_id}")
async def delete_task(task_id: UUID, user=Depends(get_current_user)):
    task = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task["user_id"] != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    await database.execute(tasks.delete().where(tasks.c.id == task_id))
    return {"msg": "Task deleted"}

@router.post("/tasks/{task_id}/complete", response_model=TaskOut)
async def complete_task(task_id: UUID, user=Depends(get_current_user)):
    task = await database.fetch_one(tasks.select().where(tasks.c.id == task_id))
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if task["user_id"] != user["username"]:
        raise HTTPException(status_code=403, detail="Not allowed")

    query = tasks.update().where(tasks.c.id == task_id).values(status=TaskStatus.completed)
    await database.execute(query)
    return {**task, "status": TaskStatus.completed}
