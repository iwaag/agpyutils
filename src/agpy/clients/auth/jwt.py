import json
from typing import Optional

import jwt

from agpy.clients.auth.config import OIDC_AUDIENCE, OIDC_ISSUER, require_config
from agpy.clients.auth.jwks import fetch_jwks, get_jwks
from agpy.contracts.auth.jwt import AuthInfo, JWTAuthError


def find_signing_key(jwks: dict, kid: str | None) -> Optional[dict]:
    if not kid:
        return None
    for key in jwks.get("keys", []):
        if key.get("kid") == kid:
            return key
    return None


async def auth_info_from_bearer_token(token: str) -> AuthInfo:
    try:
        headers = jwt.get_unverified_header(token)
    except jwt.PyJWTError as exc:
        raise JWTAuthError("Invalid token header") from exc

    jwks = await get_jwks()
    signing_key = find_signing_key(jwks, headers.get("kid"))
    if signing_key is None:
        jwks = await fetch_jwks()
        signing_key = find_signing_key(jwks, headers.get("kid"))
        if signing_key is None:
            raise JWTAuthError("Signing key not found")

    oidc_issuer = require_config(OIDC_ISSUER, "OIDC_ISSUER")
    options = {"verify_aud": bool(OIDC_AUDIENCE)}
    try:
        public_key = jwt.algorithms.RSAAlgorithm.from_jwk(json.dumps(signing_key))
        payload = jwt.decode(
            token,
            public_key,
            algorithms=["RS256"],
            issuer=oidc_issuer,
            audience=OIDC_AUDIENCE or None,
            options=options,
        )
    except jwt.PyJWTError as exc:
        raise JWTAuthError("Invalid token") from exc

    user_id = payload.get("sub")
    if not user_id:
        raise JWTAuthError("Missing sub")

    client_id = payload.get("azp")
    if not client_id:
        raise JWTAuthError("Missing azp")

    return AuthInfo(user_id=user_id, client_id=client_id, token=token)
