import json
import os
import time
from typing import Optional, Tuple

import httpx
import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

KEYCLOAK_URL = os.getenv("KEYCLOAK_URL", "http://localhost:8080")
KEYCLOAK_REALM = os.getenv("KEYCLOAK_REALM", "default_realm")
KEYCLOAK_ISSUER = os.getenv(
    "KEYCLOAK_ISSUER",
    f"{KEYCLOAK_URL}/realms/{KEYCLOAK_REALM}",
)
KEYCLOAK_AUDIENCE = os.getenv("KEYCLOAK_AUDIENCE", "").strip()
JWKS_CACHE_SECONDS = int(os.getenv("JWKS_CACHE_SECONDS", "300"))

_bearer_scheme = HTTPBearer(auto_error=False)
_jwks_cache: Optional[dict] = None
_jwks_cache_expires_at = 0.0


def _jwks_url() -> str:
    return f"{KEYCLOAK_ISSUER}/protocol/openid-connect/certs"


async def _fetch_jwks() -> dict:
    async with httpx.AsyncClient(timeout=5.0) as client:
        response = await client.get(_jwks_url())
        response.raise_for_status()
        return response.json()


async def _get_jwks() -> dict:
    global _jwks_cache, _jwks_cache_expires_at
    now = time.time()
    if _jwks_cache and now < _jwks_cache_expires_at:
        return _jwks_cache

    jwks = await _fetch_jwks()
    _jwks_cache = jwks
    _jwks_cache_expires_at = now + JWKS_CACHE_SECONDS
    return jwks


def _find_signing_key(jwks: dict, kid: str | None) -> Optional[dict]:
    if not kid:
        return None
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None

async def get_current_user_id_and_client_id(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(_bearer_scheme),
) -> Tuple[str, Optional[str]]:
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing token")

    token = credentials.credentials
    try:
        headers = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token header"
        ) from exc

    jwks = await _get_jwks()
    signing_key = _find_signing_key(jwks, headers.get("kid"))
    if signing_key is None:
        jwks = await _fetch_jwks()
        signing_key = _find_signing_key(jwks, headers.get("kid"))
        if signing_key is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="Signing key not found"
            )

    options = {"verify_aud": bool(KEYCLOAK_AUDIENCE)}
    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(signing_key))
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=KEYCLOAK_ISSUER,
            audience=KEYCLOAK_AUDIENCE or None,
            options=options,
        )
    except jwt.PyJWTError as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token"
        ) from exc

    user_id = payload.get("sub")
    if not user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing sub")

    client_id = payload.get("azp")
    if not client_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing azp")
    
    return user_id, client_id
