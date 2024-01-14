from common.models import BaseModel
from tortoise import fields


class Group(BaseModel):
    name = fields.CharField(max_length=255)
    owner = fields.ForeignKeyField('models.User', related_name='owner_groups')
    admin = fields.ForeignKeyField('models.User', related_name='admin_groups')

    class Meta:
        ordering = ['name']


class GroupUser(BaseModel):
    group = fields.ForeignKeyField('models.Group', related_name='users')
    user = fields.ForeignKeyField('models.User', related_name='groups')

    class Meta:
        unique_together = ['group', 'user']
