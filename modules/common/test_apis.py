import random
import string

from fastapi import APIRouter, Response

from modules.common.models import Tag
from modules.communication.models import Communication
from modules.user.models import ContactUser, User
from modules.user.utils import get_password_hash

router = APIRouter()


@router.get("/tags")
async def prepare_tags():
    """
    Add default tags.
    """

    tags = []
    for t in [
        'cool',
        'beauty',
        'giao',
        'game',
        'animal',
        'program',
        'python',
        'finance',
        'geography',
    ]:
        x = await Tag.create(key=t, description=t)
        tags.append(x)
    return Response()


@router.get("/tester")
async def prepare_tester():
    """
    Add two users to test
    """
    # add users
    users = []
    for u in ['test1', 'test2']:
        users.append(
            await User.create(
                username=u,
                nickname='nickname_' + u,
                password=get_password_hash('123123'),
                phone='131234' + ''.join(random.choices(string.digits, k=5)),
            )
        )
    test1, test2 = users

    # add to contacts
    communication = await Communication.create()
    await ContactUser.create(
        name=test2.nickname, me=test1, contact=test2, communication=communication
    )

    await ContactUser.create(
        name=test1.nickname, me=test2, contact=test1, communication=communication
    )
    return Response(content='success')
