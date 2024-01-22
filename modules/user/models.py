from tortoise import fields
from config.settings import DEFAULT_AVATAR_PATH, HTTP_ADDR, HTTP_SITE

from modules.common.models import BaseModel


class User(BaseModel):
    nickname = fields.CharField(max_length=32)
    username = fields.CharField(max_length=64, unique=True)
    phone = fields.CharField(max_length=16, unique=True, null=True)
    email = fields.CharField(max_length=255, null=True, unique=True)
    password = fields.CharField(max_length=128)
    disabled = fields.BooleanField(default=False)
    avatar = fields.CharField(max_length=255, null=True, default='default.jpg')

    tags = fields.ManyToManyField(
        "models.Tag", through="relate_user_tag", related_name="users"
    )

    class Meta:
        ordering = ['nickname']
        table = 'tb_user'

    @property
    def avatar_url(self):
        return HTTP_SITE + DEFAULT_AVATAR_PATH + self.avatar


class ContactUser(BaseModel):
    name = fields.CharField(max_length=32)  # remark name
    me = fields.ForeignKeyField('models.User', related_name='contacts')  # me
    contact = fields.ForeignKeyField('models.User')  # friend
    communication = fields.ForeignKeyField(
        'models.Communication', related_name='contact_users'
    )
    is_block = fields.BooleanField(default=False)

    deleted_time = fields.DatetimeField(null=True)

    class Meta:
        ordering = ['name']
        table = 'tb_contact_user'
        unique_together = ('me', 'contact')


# class ContactGroup(BaseModel):
#     name = fields.CharField(max_length=32)  # remark name
#     me = fields.ForeignKeyField('models.User', related_name='contacts')  # me
#     group = fields.ForeignKeyField('models.Group')  # friend
#     is_mute = fields.BooleanField(default=False)

#     class Meta:
#         ordering = ['name']
#         table = 'tb_contact_group'
#         unique_together = ('me', 'group')
