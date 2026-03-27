from datetime import datetime, timedelta
from enum import StrEnum
from pydantic import BaseModel, HttpUrl, Field
from typing import Optional

class TaskStatus(StrEnum):
    TODO = "todo"
    DOING = "doing"
    DONE = "done"

class TaskMetadata(BaseModel):
    type_id: str
    user_id: str
    project_id: str
    title: Optional[str] = None
    description: Optional[str] = None

class TaskBase(BaseModel):
    meta: TaskMetadata

class Task_UnmanagedLabor(TaskBase):
    redirect_url: HttpUrl
    hints: Optional[dict[str, str]] = None
    wait_for: timedelta = timedelta(minutes=5)

class Task_UpdageState(TaskBase):
    auth_url: HttpUrl