from common.models import BaseModel
from tortoise import fields

from modules.message.pydantics import MessageType


class Message(BaseModel):
    """
    message
    """

    id = fields.IntField(pk=True, generated=True)
    title = fields.CharField(max_length=255)
    content = fields.TextField()
    status = fields.IntField(default=0)  # 0未读 1已读
    type_enum = fields.IntEnumField(enum_type=MessageType)
    user = fields.ForeignKeyField('models.User', related_name='messages')

    class Meta:
        table = 'tb_message'

    def __str__(self):
        return self.title


class Communication(BaseModel):
    """
    communication
    """

    user = fields.ForeignKeyField('models.User', related_name='communications')
    message = fields.ForeignKeyField('models.Message', related_name='communications')

    class Meta:
        table = 'tb_communication'

    def __str__(self):
        return self.user.username
