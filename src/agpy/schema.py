from datetime import datetime
from typing import Any, Dict, List, Optional, Sequence

from pydantic import BaseModel, Field


class MissionInfo(BaseModel):
    id: str
    title: str
    repo_url: str
    instruction: str
    session_id: Optional[str] = None
    user_id: str
    project_id: str
    created_at: datetime
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None

class MissionUpdate(BaseModel):
    title: Optional[str] = None
    repo_url: Optional[str] = None
    instruction: Optional[str] = None

class MissionListInfo(BaseModel):
    missions: Sequence[MissionInfo]

class MissionCreateRequest(BaseModel):
    title: str = Field(min_length=1)
    repo_url: str = Field(min_length=1)
    instruction: str = Field(min_length=1)
    project_id: str = Field(min_length=1)


class MissionStartRequest(BaseModel):
    session_id: Optional[str] = None
    mission_id: str = Field(min_length=1)