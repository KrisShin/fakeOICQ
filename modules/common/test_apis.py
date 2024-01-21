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
        x = await Tag.create(key=t)
        tags.append(x)
    return Response(content=tags)


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
                nickname=u,
                password=get_password_hash('123123'),
                phone='131234' + random.choices(string.digits, k=5),
            )
        )
    test1, test2 = users

    # add to contacts
    communication = await Communication.create()
    contact1 = await ContactUser.create(
        me=test1, contact=test2, communication=communication
    )
    test1.contact_users.add(contact1)
    await test1.save()
    contact2 = await ContactUser.create(
        me=test2, contact=test1, communication=communication
    )
    test2.contact_users.add(contact2)
    await test2.save()
