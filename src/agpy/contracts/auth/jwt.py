from typing import Optional
from pydantic import BaseModel

class JWTAuthError(Exception):
    pass

class TokenExchangeResponse(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: Optional[str] = None
    refresh_expires_in: Optional[int] = None
    scope: Optional[str] = None
    session_state: Optional[str] = None
    not_before_policy: Optional[int] = None

class AuthInfo(BaseModel):
    user_id: str
    client_id: str
    token: str