"""FastAPI router for /api/tasks.

Routes are thin: validate input, call the service, map None → 404, return.
No SQLAlchemy imports here. No business logic here.
"""
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.services import task_service

router = APIRouter(prefix="/api/tasks", tags=["tasks"])

# Convenience type alias so every endpoint stays one-liner on the db param.
DbDep = Annotated[AsyncSession, Depends(get_db)]


# ---------------------------------------------------------------------------
# GET /api/tasks
# ---------------------------------------------------------------------------

@router.get(
    "",
    response_model=list[TaskResponse],
    response_model_by_alias=True,   # assigned_role → assignedRole, created_at → createdAt
    summary="List all tasks",
)
async def list_tasks(db: DbDep) -> list[Task]:
    return await task_service.get_all_tasks(db)


# ---------------------------------------------------------------------------
# POST /api/tasks
# ---------------------------------------------------------------------------

@router.post(
    "",
    response_model=TaskResponse,
    response_model_by_alias=True,
    status_code=status.HTTP_201_CREATED,
    summary="Create a task",
)
async def create_task(data: TaskCreate, db: DbDep) -> Task:
    return await task_service.create_task(db, data)


# ---------------------------------------------------------------------------
# PUT /api/tasks/{task_id}
# ---------------------------------------------------------------------------

@router.put(
    "/{task_id}",
    response_model=TaskResponse,
    response_model_by_alias=True,
    summary="Update a task (partial)",
)
async def update_task(task_id: int, data: TaskUpdate, db: DbDep) -> Task:
    task = await task_service.update_task(db, task_id, data)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
    return task


# ---------------------------------------------------------------------------
# DELETE /api/tasks/{task_id}
# ---------------------------------------------------------------------------

@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Delete a task",
)
async def delete_task(task_id: int, db: DbDep) -> None:
    deleted = await task_service.delete_task(db, task_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task {task_id} not found",
        )
