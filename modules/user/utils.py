from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

from fastapi import Depends
from jose import JWTError, jwt
from passlib.context import CryptContext
from tortoise.expressions import Q

from config.settings import ACCESS_TOKEN_EXPIRE_DAYS, ALGORITHM, SECRET_KEY
from modules.common.exceptions import AuthorizationFailed
from modules.common.global_variable import oauth2_scheme
from modules.common.pydantics import UserOpration
from modules.common.redis_client import cache_client
from modules.communication.models import Communication
from modules.user.models import ContactUser, User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str):
    """Check plain password whether right or not"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    """Generate password hashed value."""
    return pwd_context.hash(password)


def create_access_token(user_id: UUID, expires_delta: Optional[timedelta] = None):
    """create user access token"""
    to_encode = {'user_id': str(user_id)}
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def validate_token(token: str = Depends(oauth2_scheme)) -> str | bool:
    """if validate return user_id otherwise return False"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("user_id")
        expire_time: float = payload.get('exp')
        saved_token = await cache_client.get_cache(user_id)
        if (
            (user_id is None)
            or (datetime.fromtimestamp(expire_time) < datetime.utcnow())
            or (saved_token != token)
        ):
            return False
    except JWTError:
        return False
    return user_id


async def check_login_failed_cache(user_id: str):
    login_failed_key = cache_client.generate_user_operation_key(
        user_id, UserOpration.LOGIN_FAILED
    )
    login_failed_times = await cache_client.get_cache(login_failed_key)
    if (
        login_failed_times
        and login_failed_times >= UserOpration.LOGIN_FAILED.value.limit
    ):
        raise AuthorizationFailed()
    await cache_client.expire_cache(
        user_id, ex=timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )


async def get_current_user_model(user_id: str = Depends(validate_token)):
    """return user orm"""
    if user_id is False:
        raise AuthorizationFailed()
    await check_login_failed_cache(user_id)

    user = await User.get_or_none(id=user_id, disabled=False)
    return user


async def add_to_contacts(user: User, contact: User, is_block: bool = False):
    """
    make two user become contact or blacklist.
    """
    if user.id == contact.id:
        return False
    communication = await Communication.create()
    await ContactUser.create(
        name=contact.nickname,
        me=user,
        contact=contact,
        communication=communication,
        is_block=is_block,
    )
    await ContactUser.create(
        name=user.nickname,
        me=contact,
        contact=user,
        communication=communication,
        is_block=is_block,
    )


async def get_relations(me: User, contact: User):
    return await ContactUser.filter(
        Q(Q(me=me, contact=contact), Q(me=contact, contact=me), join_type=Q.OR)
    )
