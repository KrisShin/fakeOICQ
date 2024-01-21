from tortoise import fields

from modules.common.models import BaseModel
from modules.communication.pydantics import MessageType


class Message(BaseModel):
    """
    message
    """

    content = fields.TextField()
    # status = fields.IntField(default=0)  # 0未读 1已读
    message_category = fields.IntEnumField(enum_type=MessageType)

    contact_id = fields.CharField(max_length=32, index=True, null=False)
    communication_id = fields.CharField(max_length=32, index=True, null=False)

    class Meta:
        table = 'tb_message'

    def __str__(self):
        return self.title


class Communication(BaseModel):
    """
    communication
    """

    latest_message = fields.ForeignKeyField('models.Message', null=True)
    has_history = fields.BooleanField(default=False)
    new_count = fields.IntField(default=0)

    class Meta:
        ordering = ['-created_at']
        table = 'tb_communication'

    @property
    def is_valid(self):
        # TODO: check two users relationship
        return True
