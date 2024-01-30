from fastapi import APIRouter, Depends
from tortoise.expressions import Q

from modules.common.exceptions import BadRequest, NotFound, TooManyRequest
from modules.common.global_variable import BaseResponse
from modules.common.pydantics import UserOpration
from modules.common.redis_client import cache_client
from modules.common.utils import queryset_to_pydantic_model
from modules.communication.pydantics import CommunicationPydantic
from modules.user.models import (
    ContactRequest,
    ContactRequestTypeEnum,
    ContactUser,
    User,
)
from modules.user.pydantics import (
    ContactBlockOperatePydantic,
    ContactListPydantic,
    ContactRemarkPydantic,
    ContactRequestInfoPydantic,
    ContactRequestPydantic,
    ContactSearchPydantic,
    ContactUserInfoPydantic,
    MyIDPydantic,
    RequestOperatePydantic,
    UserInfoPydantic,
)
from modules.user.utils import add_to_contacts, get_current_user_model, get_relations

router = APIRouter()


@router.get('/list/')
async def get_contact_list(
    is_block: str,
    offset: str = 0,
    page_size: str = 10,
    me: User = Depends(get_current_user_model),
):
    """
    Get contact list/blacklist\n
    @params:\n
        is_block: bool default False
        offset: int page * page_size
        page_size: int default 10
    """
    params = ContactListPydantic(is_block=is_block, offset=offset, page_size=page_size)
    contact_queryset = (
        await ContactUser.filter(me=me)
        .filter(deleted_time=None, is_block=params.is_block)
        .offset(params.offset)
        .limit(params.page_size)
    )
    return queryset_to_pydantic_model(contact_queryset, ContactUserInfoPydantic)


@router.post('/search/')
async def post_contact_search(
    params: ContactSearchPydantic,
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

    contact_id_list = await ContactUser.filter(me=me, deleted_time=None).values_list(
        'contact__id', flat=True
    )
    contact_id_list.append(me.id)
    user_queryset = (
        await User.filter(id__not_in=contact_id_list)
        .filter(
            Q(
                Q(username=params.query),
                Q(email=params.query),
                Q(phone=params.query),
                Q(nickname__icontains=params.query),
                join_type=Q.OR,
            )
        )
        .offset(params.offset)
        .limit(params.page_size)
    )
    return queryset_to_pydantic_model(user_queryset, UserInfoPydantic)


@router.post('/request/')
async def post_contact_request(
    params: ContactRequestPydantic,
    me: User = Depends(get_current_user_model),
):
    """
    Request to be contact.\n
    @params:\n
        contact_id: id of user who be searched.
        message: str
    """
    times = await cache_client.get_cache(me.id, UserOpration.ADD_CONTACT)
    if times > UserOpration.EDIT_PASSWORD.value.limit:
        raise TooManyRequest('Request limited.')
    contact = await User.get_or_none(id=params.id)
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
        message=params.message,
    )
    await cache_client.limit_opt_cache(me.id, UserOpration.ADD_CONTACT)
    return BaseResponse()


@router.get('/request/list/')
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
    resp = queryset_to_pydantic_model(
        pendding_request_queryset, ContactRequestInfoPydantic
    )
    resp.extend(
        queryset_to_pydantic_model(other_request_queryset, ContactRequestInfoPydantic)
    )
    return BaseResponse(data=resp)


@router.put('/request/operate/')
async def put_contact_request_operate(
    params: RequestOperatePydantic, me: User = Depends(get_current_user_model)
):
    """
    Operate contact request.\n
    @params:\n
        request_id: str.
        operate: bool: True/False
    """
    request = await ContactRequest.get_or_none(
        id=params.id, contact=me, status=ContactRequestTypeEnum.REQUEST
    ).prefetch_related('me')
    if not request:
        raise NotFound('Request not found.')
    if params.operate:
        request.status = ContactRequestTypeEnum.ACCEPT
        res = await add_to_contacts(me, request.me)
        if res is False:
            raise BadRequest("Can't be friend with yourself.")
    else:
        request.reply = params.message
        request.status = ContactRequestTypeEnum.DECLINE
    await request.save()
    return BaseResponse()


@router.put('/block/')
async def put_contact_operate(
    params: ContactBlockOperatePydantic, me: User = Depends(get_current_user_model)
):
    """
    block/unblock contact.\n
    @params:\n
        user_id: str.
        is_block: bool: True/False
    """
    user = await User.get_or_none(id=params.id)
    if not user:
        raise NotFound('User not found.')

    relation1, relation2 = await get_relations(me, user)
    if not relation1:
        if params.is_block:
            res = await add_to_contacts(me, user, is_block=params.is_block)
            if res is False:
                raise BadRequest("Can't block yourself.")
        raise BadRequest('Cannot unblock user who is not contact.')
    else:
        relation1.is_block = params.is_block
        relation2.is_block = params.is_block
        await relation1.save()
        await relation2.save()

    return BaseResponse('relationship is blocked')


@router.delete('/')
async def delete_contact(
    params: MyIDPydantic, me: User = Depends(get_current_user_model)
):
    """
    Operate contact request.\n
    @params:\n
        user_id: str.
        operate: bool: True/False
    """
    user = await User.get_or_none(id=params.id)
    if not user:
        raise NotFound('User not found.')

    relation1, relation2 = await get_relations(me, user)
    if not all((relation1, relation2)):
        raise BadRequest('Cannot unblock user who is not contact.')
    else:
        await relation1.delete()
        await relation2.delete()

    return BaseResponse('contact is delete')


@router.put('/remark/')
async def put_contact_remark(
    params: ContactRemarkPydantic, me: User = Depends(get_current_user_model)
):
    """
    Remark contact.\n
    @params:\n
        user_id: str.
        remark: str.
    """
    user = await User.get_or_none(id=params.id)
    if not user:
        raise NotFound('User not found.')
    contact = await ContactUser.get_or_none(me=me, contact=user)
    if not contact:
        raise NotFound('User is not you contact.')

    contact.name = params.remark or user.nickname
    await contact.save()
    return BaseResponse()


@router.get('/{contact_id}/')
async def get_contact_info(contact_id: str, me: User = Depends(get_current_user_model)):
    """
    Get contact communication infomation.
    """
    contact = await ContactUser.get_or_none(id=contact_id).prefetch_related(
        'communication'
    )
    resp = {
        'contact': ContactUserInfoPydantic.model_validate(contact).model_dump(),
        'communication': CommunicationPydantic.model_validate(
            contact.communication
        ).model_dump(),
    }
    return BaseResponse(data=resp)
