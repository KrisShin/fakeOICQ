from pydantic import BaseModel
from tortoise.contrib.pydantic import pydantic_model_creator

from modules.user.models import ContactUser, User


class UserLoginPydantic(BaseModel):
    username: str
    password: str


UserPydantic = pydantic_model_creator(User, name="UserPydantic")

UserInfoPydantic = pydantic_model_creator(
    User,
    name="UserInfo",
    exclude=('password', 'create_time', 'update_time', 'disabled'),
)
ContactUserInfoPydantic = pydantic_model_creator(
    ContactUser,
    name="ContactUserInfo",
)


class TokenPydantic(BaseModel):
    access_token: str
    token_type: str = 'Bearer'
