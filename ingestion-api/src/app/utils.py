from typing import Annotated, Any
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from shared.shared_utils import decode_and_validate_token
    
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/location/send', auto_error=False)

def get_token(token: str | None = Depends(oauth2_scheme)):
    if token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='No authorization token found'
        )
    try:
        payload = decode_and_validate_token(token)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
        )

    return payload
    
auth_dependency = Annotated[dict[str, Any], Depends(get_token)]