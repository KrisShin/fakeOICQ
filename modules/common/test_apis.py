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
    for u in ['test1', 'test2', 'test3', 'test4']:
        users.append(
            await User.create(
                username=u,
                nickname='nickname_' + u,
                password=get_password_hash('123123'),
                phone='131234' + ''.join(random.choices(string.digits, k=5)),
            )
        )
    t1,t2,t3,t4 = users

    tags = await Tag.all()

    async def _set_random_tags(user: User, n: int):
        for t in random.choices(tags, k=n):
            await user.tags.add(t)

    await _set_random_tags(t1, random.randint(1, 5))
    await _set_random_tags(t2, random.randint(1, 5))
    await _set_random_tags(t3, random.randint(1, 5))
    await _set_random_tags(t4, random.randint(1, 5))

    # add to contacts

    async def _add_to_contacts(user: User, contacts: list[User]):
        communication = await Communication.create()
        await ContactUser.create(
            name=contacts.nickname, me=user, contact=contacts, communication=communication
        )
        await ContactUser.create(
            name=user.nickname, me=contacts, contact=user, communication=communication
        )
    await _add_to_contacts(t1, t2)
    await _add_to_contacts(t1, t3)
    await _add_to_contacts(t1, t4)
    await _add_to_contacts(t2, t3)
    await _add_to_contacts(t3, t4)
    return Response(content='success')
