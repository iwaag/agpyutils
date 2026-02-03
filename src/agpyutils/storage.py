from typing import List
import httpx
import os
from pydantic import BaseModel

class StorageResourceRef(BaseModel):
    key: str
    domain: str
    project: str | None = None
    is_staging: bool = False
    is_package: bool = False

class ResuorceInfo(StorageResourceRef):
    sub_resources: List[StorageResourceRef]

class PresignUploadRequest(StorageResourceRef):
    expires_in: int | None = None
    content_type: str | None = None

class PresignDownloadRequest(BaseModel):
    storate_resource_id: str
    expires_in: int | None = None
    response_content_type: str | None = None
    response_content_disposition: str | None = None

class CopyObjectRequest(BaseModel):
    source: StorageResourceRef
    destination: StorageResourceRef

STORAGE_SERVICE_URL=os.getenv("STORAGE_SERVICE_URL")
DOWNLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/download"
UPLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/upload"
COPY_URL=f"{STORAGE_SERVICE_URL}/s3/copy"
DELETE_URL=f"{STORAGE_SERVICE_URL}/s3/delete"
MOVE_URL=f"{STORAGE_SERVICE_URL}/s3/move"
async def get_download_url(auth_header: str, request: PresignDownloadRequest) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            DOWNLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            #json={"domain": domain, "key": key, "is_staging": is_staging},
            json=request.model_dump()
        )
        return response.json()["url"]

async def get_upload_url(auth_header: str, request: PresignUploadRequest) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            UPLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            json=request.model_dump()
        )
        return response.json()["url"]

async def copy(
    auth_header: str,
    request: CopyObjectRequest
) -> str:
    #payload = {
    #    "source": {"key": source_key, "domain": source_domain, "staging": source_staging},
    #    "destination": {"key": destination_key, "domain": destination_domain, "staging": destination_staging},
    #}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            COPY_URL,
            headers={"authorization": auth_header},
            json=request.model_dump()
        )
async def delete(
    auth_header: str,
    object_ref: StorageResourceRef
) -> str:
    #payload = {
    #    "source": {"key": source_key, "domain": source_domain, "staging": source_staging},
    #    "destination": {"key": destination_key, "domain": destination_domain, "staging": destination_staging},
    #}
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
    #payload = {
    #    "source": {"key": source_key, "domain": source_domain, "staging": source_staging},
    #    "destination": {"key": destination_key, "domain": destination_domain, "staging": destination_staging},
    #}
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            MOVE_URL,
            headers={"authorization": auth_header},
            json=request.model_dump()
        )