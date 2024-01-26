from tortoise import fields

from modules.common.models import BaseModel


class Notification(BaseModel):
    """
    Notifacation.
    """

    ...

    class Meta:
        table = "tb_notification"
        unique_together = (("user_id", "title"),)
        ordering = ["-create_time"]
