from tortoise import fields, models

from modules.common.utils import generate_random_id


class BaseModel(models.Model):
    id = fields.CharField(primary_key=True, max_length=32, default=generate_random_id)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)
