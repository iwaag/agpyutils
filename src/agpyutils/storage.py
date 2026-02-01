import httpx
import os

STORAGE_SERVICE_URL=os.getenv("STORAGE_SERVICE_URL")
DOWNLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/download"
UPLOAD_PRESIGN_URL=f"{STORAGE_SERVICE_URL}/s3/presign/upload"
async def get_download_url(auth_header: str, domain: str, key: str, is_staging: bool) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            DOWNLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            json={"domain": domain, "key": key, "is_staging": is_staging},
        )
        return response.json()["url"]

async def get_upload_url(auth_header: str, domain: str, key: str, is_staging: bool) -> str:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.post(
            UPLOAD_PRESIGN_URL,
            headers={"authorization": auth_header},
            json={"domain": domain, "key": key, "is_staging": is_staging},
        )
        return response.json()["url"]