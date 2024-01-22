from datetime import timedelta

from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import ACCESS_TOKEN_EXPIRE_DAYS
from modules.common.exceptions import AuthenticationFailed
from modules.common.utils import del_cache, queryset_to_pydantic_model, set_cache
from modules.user.models import ContactUser, User
from modules.user.pydantics import (
    ContactUserInfoPydantic,
    TokenPydantic,
    UserInfoPydantic,
    UserRegisterPydantic,
)
from modules.user.utils import (
    create_access_token,
    get_current_user_model,
    get_password_hash,
    verify_password,
)

router = APIRouter()


@router.post('/register/')
async def post_register_user(user: UserRegisterPydantic):
    """
    regester user\n
    @params:\n
        username :str
        password :str
    @default phone None\n
            nickname username :You can modify later.
    """
    password_hash = get_password_hash(user.password)
    user_obj = await User.get_or_none(username=user.username)
    if not user_obj:
        user_obj = await User.create(
            nickname=user.username,
            username=user.username,
            password=password_hash,
        )
        response_data = UserInfoPydantic.model_validate(user_obj)
        return response_data
    raise AuthenticationFailed('User already exist.')


@router.post('/reset_password/')
async def post_reset_password(username):
    """
    reset user's password to '123123'.\n
    maybe just for test or just reset my password.\n
    @params:\n
        username :str will delete later.
    """
    user_obj = await User.get_or_none(username=username)
    if user_obj:
        password_hash = get_password_hash('123123')
        user_obj.password = password_hash
        await user_obj.save()
        return TokenPydantic(access_token=create_access_token(user_obj.id))
    raise AuthenticationFailed('username not exist.')


@router.post('/token/', response_model=TokenPydantic)
async def post_user_token(
    request: Request, user: OAuth2PasswordRequestForm = Depends()
):
    user_obj = await User.get_or_none(username=user.username)
    if not user_obj or (user and user_obj.disabled):
        raise AuthenticationFailed('Username exist.')
    if not verify_password(user.password, user_obj.password):
        return AuthenticationFailed('Wrong password')
    access_token_expires = timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    token = create_access_token(user_id=user_obj.id, expires_delta=access_token_expires)
    await del_cache(str(user_obj.id))
    await set_cache(str(user_obj.id), token, access_token_expires)
    resp = TokenPydantic(access_token=token)
    return resp


@router.get('/me/')
async def get_me_detail(user: User = Depends(get_current_user_model)):
    user_base_info = UserInfoPydantic.model_validate(user).model_dump()
    user_base_info['avatar_url'] = user.avatar_url
    contact_list = (
        await ContactUser.filter(me=user)
        .filter(deleted_time=None, is_block=False)
        .limit(10)
    )
    user_base_info['contacts'] = queryset_to_pydantic_model(
        contact_list, ContactUserInfoPydantic
    )
    return user_base_info


@router.get('/contact/list')
async def get_contact_list(
    is_block: bool = False,
    offset: int = 0,
    page_size: int = 10,
    user: User = Depends(get_current_user_model),
):
    """
    Get contact list/blacklist\n
    @params:\n
        is_block: str default False
        offset: int page * page_size
        page_size: int default 10
    """
    if is_block:
        is_block = is_block.strip().lower() in ('true', '1', 't', 'yes')
    contact_list = (
        await ContactUser.filter(me=user)
        .filter(deleted_time=None, is_block=is_block)
        .offset(offset)
        .limit(page_size)
    )
    resp = queryset_to_pydantic_model(contact_list, ContactUserInfoPydantic)
    return resp
