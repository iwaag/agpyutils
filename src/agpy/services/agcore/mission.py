import os
from typing import override

from hatchet_sdk import client
import httpx

from agpy.contracts.agcore.mission import (
    MissionCreateRequest,
    MissionInfo,
    MissionListInfo,
    MissionUpdate,
)

from agpy.auth import AuthInfo

AGCORE_API_URL=os.getenv("AGCORE_API_URL")
async def get_mission(self, mission_id: str, auth_info: AuthInfo) -> MissionListInfo:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            AGCORE_API_URL + f"/mission/get/{mission_id}",
            headers={"authorization": "bearer " + auth_info.auth_token}
        )
        return MissionListInfo.model_validate(response.json())

async def create_mission(request: MissionCreateRequest, auth_info: AuthInfo) -> MissionInfo:
    pass

async def list_missions() -> MissionListInfo:
    pass

async def complete_mission(mission_id: str, auth: AuthInfo) -> MissionListInfo:
    pass