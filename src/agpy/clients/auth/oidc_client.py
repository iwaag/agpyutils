import httpx

from agpy.clients.auth.config import (
    CLIENT_ID,
    OIDC_CLIENT_SECRET,
    OIDC_TOKEN_ENDPOINT,
    require_config,
)
from agpy.contracts.auth.jwt import JWTAuthError, TokenExchangeResponse


async def exchange_token_for_own_client(
    subject_token: str,
    timeout_seconds: float = 5.0,
) -> TokenExchangeResponse:
    if not CLIENT_ID:
        raise JWTAuthError("CLIENT_ID is not configured")

    oidc_token_endpoint = require_config(OIDC_TOKEN_ENDPOINT, "OIDC_TOKEN_ENDPOINT")
    form_data = {
        "grant_type": "urn:ietf:params:oauth:grant-type:token-exchange",
        "client_id": CLIENT_ID,
        "subject_token": subject_token,
        "subject_token_type": "urn:ietf:params:oauth:token-type:access_token",
        "requested_token_type": "urn:ietf:params:oauth:token-type:access_token",
    }
    if OIDC_CLIENT_SECRET:
        form_data["client_secret"] = OIDC_CLIENT_SECRET

    async with httpx.AsyncClient(timeout=timeout_seconds) as client:
        response = await client.post(oidc_token_endpoint, data=form_data)

    if response.status_code >= 400:
        raise JWTAuthError(
            f"Token exchange failed ({response.status_code}): {response.text}"
        )

    return TokenExchangeResponse.model_validate(response.json())


async def issue_own_client_access_token(
    subject_token: str,
    timeout_seconds: float = 5.0,
) -> str:
    token_response = await exchange_token_for_own_client(
        subject_token=subject_token,
        timeout_seconds=timeout_seconds,
    )
    return token_response.access_token
