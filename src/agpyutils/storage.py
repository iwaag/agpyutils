from typing import List
import httpx
import os
from pydantic import BaseModel

class BaseResourceRef(BaseModel):
    domain: str
    user_id: str
    project: str | None = None

class StaticObjectRef(BaseResourceRef):
    relative_key: str

class NewDynamicObjectGroupRequest(BaseResourceRef):
    caetegory: str

class DynamicObjectRef(BaseResourceRef):
    group_id: str
    relative_key: str

class PresignUploadOption(BaseModel):
    expires_in: int = 3600
    content_type: str | None = None

class PresignDownloadOption(BaseModel):
    expires_in: int = 3600
    response_content_type: str | None = None
    response_content_disposition: str | None = None

class CopyObjectRequest(BaseModel):
    source_strage_resource_id: str
    destination_strage_resource_id: str

STORAGE_SERVICE_URL=os.getenv("STORAGE_SERVICE_URL")
STATIC_DOWNLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/static_object/download"
STATIC_UPLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/static_object/upload"
DYNAMIC_DOWNLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/dynamic_object/download"
DYNAMIC_UPLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/dynamic_object/upload"

async def get_static_object_download_url(
    auth_header: str,
    object_ref: StaticObjectRef,
    option: PresignDownloadOption = PresignDownloadOption()
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            STATIC_DOWNLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            json={"ref": object_ref, "option": option.model_dump()}
        )
        return response.json()["url"]

async def get_static_object_upload_url(
    auth_header: str,
    object_ref: StaticObjectRef, 
    option: PresignUploadOption = PresignUploadOption()
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            STATIC_UPLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            json={"ref": object_ref, "option": option.model_dump()}
        )
        return response.json()["url"]


# async def copy(
#     auth_header: str,
#     request: CopyObjectRequest
# ) -> str:
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.post(
#             COPY_URL,
#             headers={"authorization": auth_header},
#             json=request.model_dump()
#         )
# async def delete(
#     auth_header: str,
#     object_ref: DynamicObjectRef
# ) -> str:
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.post(
#             DELETE_URL,
#             headers={"authorization": auth_header},
#             json=object_ref.model_dump()
#         )
# async def move(
#     auth_header: str,
#     request: CopyObjectRequest
# ) -> str:
#     async with httpx.AsyncClient(timeout=5.0) as client:
#         response = await client.post(
#             MOVE_URL,
#             headers={"authorization": auth_header},
#             json=request.model_dump()
#         )