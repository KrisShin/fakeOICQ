from common.models import BaseModel
from tortoise import fields


class User(BaseModel):
    nickname = fields.CharField(max_length=32)
    username = fields.CharField(max_length=64, unique=True)
    phone = fields.CharField(max_length=16, unique=True)
    password = fields.CharField(max_length=128)
    avatar = fields.CharField(max_length=255, null=True, default='default.jpg')
    contacts = fields.ManyToManyField(
        'models.Contact', related_name='users', through='Contact'
    )

    class Meta:
        ordering = ['nickname']
        table = 'tb_user'


class Contact(BaseModel):
    name = fields.CharField(max_length=32)
    user = fields.ForeignKeyField('models.User', related_name='contacts')
    is_block = fields.BooleanField(default=False)

    class Meta:
        ordering = ['name']
        table = 'tb_contact'
