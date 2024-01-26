import os
import re
import string
from typing import List

from pydantic import BaseModel, field_validator
from tortoise.contrib.pydantic import pydantic_model_creator

from config.settings import BASE_DIR, DEBUG, DEFAULT_AVATAR_PATH
from modules.user.models import ContactRequest, ContactUser, User

UserPydantic = pydantic_model_creator(User, name="UserPydantic")

UserInfoPydantic = pydantic_model_creator(
    User,
    name="UserInfo",
    exclude=('password', 'create_time', 'update_time', 'disabled', 'avatar'),
)

ContactUserInfoPydantic = pydantic_model_creator(
    ContactUser,
    name="ContactUserInfo",
)

ContactRequestInfoPydantic = pydantic_model_creator(
    ContactRequest,
    name="ContactRequestInfo",
)


class UserRegisterPydantic(BaseModel):
    username: str
    password: str


class TokenPydantic(BaseModel):
    access_token: str
    token_type: str = 'Bearer'


class PagiantionPydantic(BaseModel):
    offset: int = 0
    page_size: int = 10

    @field_validator('offset')
    def validate_offset(cls, v):
        try:
            return int(v)
        except:
            return 0

    @field_validator('page_size')
    def validate_page_size(cls, v):
        try:
            return int(v)
        except:
            return 10


class ContactBlockPydantic(BaseModel):
    is_block: str

    @field_validator('is_block')
    def validate_is_block(cls, v):
        if v:
            return v.strip().lower() in ('true', '1', 't', 'yes')
        return False


class ContactListPydantic(PagiantionPydantic, ContactBlockPydantic):
    ...


class ContactSearchPydantic(PagiantionPydantic):
    query: str

    @field_validator('query')
    def validate_query(cls, v):
        v = v.strip()
        if not v:
            raise ValueError('query can not be empty')
        return v


class MyIDPydantic(BaseModel):
    id: str

    @field_validator('id')
    def validate_id(cls, v):
        if not v or len(v) != 32:
            raise ValueError('not a validate id.')
        return v


class ContactRequestPydantic(MyIDPydantic):
    message: str = ''


class RequestOperatePydantic(ContactRequestPydantic):
    operate: bool


class ContactBlockOperatePydantic(MyIDPydantic, ContactBlockPydantic):
    ...


class ContactRemarkPydantic(MyIDPydantic):
    remark: str = ''

    @field_validator('remark')
    def validate_remark(cls, v):
        if not v or v.strip() == '':
            return False
        return v.strip()


class UserEditPydantic(MyIDPydantic):
    phone: str = ''
    email: str = ''
    nickname: str
    avatar: str = ''
    tags: List[str] = []

    @field_validator('phone')
    def validate_phone(cls, v):
        if v and not re.match(r'^1[3-9]\d{9}$', v):
            raise ValueError('not a validate phone number.')
        return v

    @field_validator('email')
    def validate_email(cls, v):
        if v and not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', v):
            raise ValueError('not a validate email address.')
        return v

    @field_validator('nickname')
    def validate_nickname(cls, v):
        return v and v.strip()

    @field_validator('avatar')
    def validate_avatar(cls, v):
        if v and not os.path.exists(
            os.path.join(os.path.join(BASE_DIR, DEFAULT_AVATAR_PATH), v)
        ):
            raise ValueError('avatar file not exist')
        return 'default.jpg'


class UserEditPasswordPydantic(BaseModel):
    old_password: str
    new_password: str

    @field_validator('old_password')
    def validate_old_password(cls, v):
        v = v.strip()
        if not v or v == '':
            raise ValueError('old password is empty')
        return v

    @field_validator('new_password')
    def validate_new_password(cls, v: str):
        v = v.strip()
        if len(v) < 6:
            raise ValueError('new password is too short')
        if not DEBUG:
            v_set = set(list(v))
            upper_set = set(list(string.ascii_lowercase))
            lower_set = set(list(string.ascii_uppercase))
            digits_set = set(list(string.digits))
            if (
                v_set == v_set - upper_set
                or v_set == v_set - lower_set
                or v_set == v_set - digits_set
                or not v_set - upper_set - lower_set - digits_set
            ):
                raise ValueError('new password is too simple')
        return v
