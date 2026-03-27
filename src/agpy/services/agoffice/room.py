from agpy.contracts.agcore.mission import (
    MissionInfo,
    MissionStartRequest
)

from agpy.auth import AuthInfo

async def start_mission(request: MissionStartRequest, AuthInfo: AuthInfo) -> MissionInfo:
    pass