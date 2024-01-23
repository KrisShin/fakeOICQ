from datetime import timedelta

from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from tortoise.expressions import Q

from config.settings import ACCESS_TOKEN_EXPIRE_DAYS
from modules.common.exceptions import AuthenticationFailed, BadRequest, NotFound
from modules.common.utils import del_cache, queryset_to_pydantic_model, set_cache
from modules.user.models import (
    ContactRequest,
    ContactRequestTypeEnum,
    ContactUser,
    User,
)
from modules.user.pydantics import (
    ContactRequestPydantic,
    ContactUserInfoPydantic,
    TokenPydantic,
    UserInfoPydantic,
    UserRegisterPydantic,
)
from modules.user.utils import (
    add_to_contacts,
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
async def post_user_token(user: OAuth2PasswordRequestForm = Depends()):
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
async def get_me_detail(me: User = Depends(get_current_user_model)):
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
    return user_base_info


@router.get('/contact/list')
async def get_contact_list(
    is_block: bool = False,
    offset: int = 0,
    page_size: int = 10,
    me: User = Depends(get_current_user_model),
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
    contact_queryset = (
        await ContactUser.filter(me=me)
        .filter(deleted_time=None, is_block=is_block)
        .offset(offset)
        .limit(page_size)
    )
    resp = queryset_to_pydantic_model(contact_queryset, ContactUserInfoPydantic)
    return resp


@router.post('/contact/search')
async def post_contact_search(
    query: str,
    offset: int = 0,
    page_size: int = 10,
    me: User = Depends(get_current_user_model),
):
    """
    Search user.\n
    not in contact list, not in blacklist, query can be username(Precision), email(Precision), phone(Precision), nickname(fuzzy)\n
    @params:\n
        is_block: str default False
        offset: int page * page_size
        page_size: int default 10
    """
    query = query.strip()
    if not query:
        raise NotFound('User not exist.')
    contact_id_list = await ContactUser.filter(me=me, deleted_time=None).values_list(
        'contact__id', flat=True
    )
    contact_id_list.append(me.id)
    user_queryset = (
        await User.filter(id__not_in=contact_id_list)
        .filter(
            Q(
                Q(username=query),
                Q(email=query),
                Q(phone=query),
                Q(nickname__icontains=query),
                join_type=Q.OR,
            )
        )
        .offset(offset)
        .limit(page_size)
    )
    resp = queryset_to_pydantic_model(user_queryset, UserInfoPydantic)
    return resp


@router.post('/contact/request')
async def post_contact_request(
    contact_id: str,
    message: str = '',
    me: User = Depends(get_current_user_model),
):
    """
    Request to be contact.\n
    @params:\n
        contact_id: id of user who be searched.
        message: str
    """
    contact = await User.get_or_none(id=contact_id)
    if not contact:
        raise NotFound('Wrong user id, user not exist.')
    contact_user = await ContactUser.get_or_none(me=me, contact=contact)
    if contact_user:
        raise BadRequest('Already friends or in blacklist.')
    request = await ContactRequest.get_or_none(
        me=me, contact=contact, status=ContactRequestTypeEnum.REQUEST
    )
    if request:
        raise BadRequest('Already requested, Please waitting user accept.')

    await ContactRequest.create(
        me=me,
        contact=contact,
        message=message,
    )
    return {'status': 'success'}


@router.post('/contact/request/list')
async def get_contact_request_list(me: User = Depends(get_current_user_model)):
    """
    Get list of user who requested to be contact.\n
    @params:\n
        me: user who request to be contact.
    """
    pendding_request_queryset = await ContactRequest.filter(
        contact=me,
        status=ContactRequestTypeEnum.REQUEST,
    )
    other_request_queryset = await ContactRequest.filter(
        contact=me,
    ).exclude(status=ContactRequestTypeEnum.REQUEST)
    resp = queryset_to_pydantic_model(pendding_request_queryset, ContactRequestPydantic)
    resp.extend(
        queryset_to_pydantic_model(other_request_queryset, ContactRequestPydantic)
    )
    return resp


@router.post('/contact/request/operate')
async def post_contact_request_operate(
    request_id: str, operate: bool, me: User = Depends(get_current_user_model)
):
    """
    Operate contact request.\n
    @params:\n
        request_id: str.
        operate: bool: True/False
    """
    request = await ContactRequest.get_or_none(
        id=request_id, contact=me, status=ContactRequestTypeEnum.REQUEST
    ).prefetch_related('me')
    if not request:
        raise NotFound('Request not found.')
    if operate:
        request.status = ContactRequestTypeEnum.ACCEPT
        res = await add_to_contacts(me, request.me)
        if res is False:
            raise BadRequest("Can't be friend with yourself.")
    else:
        request.status = ContactRequestTypeEnum.DECLINE
    await request.save()
    return {'status': 'ok'}
