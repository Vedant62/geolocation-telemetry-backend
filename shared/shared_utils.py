from typing import Any
from shared.config import settings
from jose import jwt, JWTError

def decode_and_validate_token(token: str) -> dict[str, Any]:
    try:
        payload = jwt.decode(
            token,
            settings.secret,
            algorithms=[settings.algorithm],
        )
        return payload
    except JWTError as e:
        raise JWTError(f"Invalid or expired JWT: {str(e)}") from e