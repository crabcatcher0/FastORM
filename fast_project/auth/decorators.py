from functools import wraps
from fastapi import HTTPException


def login_required(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        user = kwargs.get("current_user")
        if not user:
            raise HTTPException(status_code=401, detail='Unauthorized')
        return await func(*args, **kwargs)
    return wrapper