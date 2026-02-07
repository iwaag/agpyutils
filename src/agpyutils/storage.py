from typing import List
import httpx
import os
from pydantic import BaseModel

class BaseObjectRef(BaseModel):
    domain: str
    user_id: str
    project: str | None = None

class StaticObjectRef(BaseObjectRef):
    key: str

class DynamicObjectRef(BaseObjectRef):
    purpose: str
    group_id: str

class PresignUploadOption(BaseModel):
    expires_in: int | None = None
    content_type: str | None = None

class PresignDownloadOption(BaseModel):
    expires_in: int | None = None
    response_content_type: str | None = None
    response_content_disposition: str | None = None

class CopyObjectRequest(BaseModel):
    source_strage_resource_id: str
    destination_strage_resource_id: str

STORAGE_SERVICE_URL=os.getenv("STORAGE_SERVICE_URL")
DOWNLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/download"
UPLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/upload"
COPY_URL=f"{STORAGE_SERVICE_URL}/s3/copy"
DELETE_URL=f"{STORAGE_SERVICE_URL}/s3/delete"
MOVE_URL=f"{STORAGE_SERVICE_URL}/s3/move"

async def get_download_url(
    auth_header: str,
    stored_resource_id: str,
    request: PresignDownloadOption
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            DOWNLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            params={"stored_resource_id": stored_resource_id},
            json=request.model_dump()
        )
        return response.json()["url"]

async def get_upload_url(
    auth_header: str,
    stored_resource_id: str, 
    request: PresignUploadOption
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            UPLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            params={"stored_resource_id": stored_resource_id},
            json=request.model_dump()
        )
        return response.json()["url"]


async def copy(
    auth_header: str,
    request: CopyObjectRequest
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            COPY_URL,
            headers={"authorization": auth_header},
            json=request.model_dump()
        )
async def delete(
    auth_header: str,
    object_ref: DynamicObjectRef
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            DELETE_URL,
            headers={"authorization": auth_header},
            json=object_ref.model_dump()
        )
async def move(
    auth_header: str,
    request: CopyObjectRequest
) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            MOVE_URL,
            headers={"authorization": auth_header},
            json=request.model_dump()
        )