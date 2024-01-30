from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

from config.settings import ACCESS_TOKEN_EXPIRE_DAYS
from modules.common.exceptions import BadRequest, TooManyRequest
from modules.common.global_variable import BaseResponse
from modules.common.models import Tag
from modules.common.pydantics import TagPydantic, UserOpration
from modules.common.redis_client import cache_client
from modules.common.utils import queryset_to_pydantic_model
from modules.user.models import ContactUser, User
from modules.user.pydantics import (
    ContactUserInfoPydantic,
    TokenPydantic,
    UserEditPasswordPydantic,
    UserEditPydantic,
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
async def post_register(user: UserRegisterPydantic):
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
        return BaseResponse(data=response_data)
    raise BadRequest('User already exist.')


@router.post('/reset_password/')
async def post_reset_password(username: str):
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
    raise BadRequest('username not exist.')


@router.post('/token/', response_model=TokenPydantic)
async def post_token(user: OAuth2PasswordRequestForm = Depends()):
    """
    User login.
    """
    user_obj = await User.get_or_none(username=user.username)
    if not user_obj or (user and user_obj.disabled):
        raise BadRequest('User not exist.')
    if not verify_password(user.password, user_obj.password):
        await cache_client.limit_opt_cache(user_obj.id, UserOpration.LOGIN_FAILED)
        raise BadRequest('Wrong password')
    token = create_access_token(user_id=user_obj.id)
    await cache_client.set_cache(
        str(user_obj.id), token, timedelta(days=ACCESS_TOKEN_EXPIRE_DAYS)
    )
    return TokenPydantic(access_token=token)


@router.get('/me/')
async def get_me_info(me: User = Depends(get_current_user_model)):
    """
    Get my info.
    """
    user_base_info = UserInfoPydantic.model_validate(me).model_dump()
    user_base_info['avatar_url'] = me.avatar_url
    contact_queryset = (
        await ContactUser.filter(me=me)
        .filter(deleted_time=None, is_block=False)
        .limit(10)
    )
    user_base_info['contacts'] = queryset_to_pydantic_model(
        contact_queryset, ContactUserInfoPydantic
    )
    user_base_info['tags'] = queryset_to_pydantic_model(
        await me.tags.all(), TagPydantic
    )
    return BaseResponse(data=user_base_info)


@router.put('/edit/')
async def put_edit_my_info(
    params: UserEditPydantic, me: User = Depends(get_current_user_model)
):
    """
    Edit user's base info.\n
    maybe just for test or just reset my password.\n
    @params:\n
        nickname: str.
        avatar: str.
        phone: str. only edit one time.
        email: str.
        tags: list[str].
    """
    times = await cache_client.get_cache(me.id, UserOpration.EDIT_INFO)
    if times > UserOpration.EDIT_INFO.value.limit:
        raise TooManyRequest('Request limited.')
    exclude_fields = ['tags']
    if me.phone:
        exclude_fields.append('phone')
    me = await me.update_from_dict(params.model_dump(exclude=exclude_fields))
    if params.tags:
        tag_queryset = await Tag.filter(key__in=params.tags)
        await me.tags.clear()
        [await me.tags.add(tag) for tag in tag_queryset]
    await me.save()
    user_base_info = UserInfoPydantic.model_validate(me).model_dump()
    user_base_info['avatar_url'] = me.avatar_url
    user_base_info['tags'] = queryset_to_pydantic_model(
        await me.tags.all(), TagPydantic
    )
    await cache_client.limit_opt_cache(me.id, UserOpration.EDIT_INFO)
    return BaseResponse(data=user_base_info)


@router.post('/edit/password/')
async def post_edit_password(
    params: UserEditPasswordPydantic, me: User = Depends(get_current_user_model)
):
    """
    edit user's password.\n
    maybe just for test or just reset my password.\n
    @params:\n
        old_password: str,
        new_password: str, length more than 6, within uppercase lowercase and digits.
    """
    if verify_password(params.old_password, me.password):
        if verify_password(params.new_password, me.password):
            raise BadRequest('new password is same as old password')
        times = await cache_client.get_cache(me.id, UserOpration.EDIT_PASSWORD)
        if times > UserOpration.EDIT_PASSWORD.value.limit:
            raise TooManyRequest('Request limited.')
        password_hash = get_password_hash(params.new_password)
        me.password = password_hash
        await me.save()
        cache_client.del_cache(me.id)
        return BaseResponse()
    await cache_client.limit_opt_cache(me.id, UserOpration.LOGIN_FAILED)
    raise BadRequest('Wrong password.')
