from tortoise import fields, models

from modules.common.utils import generate_random_id


class BaseModel(models.Model):
    id = fields.CharField(pk=True, max_length=32, default=generate_random_id)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        abstract = True


class Tag(models.Model):
    """
    The Tag model
    """

    key = fields.CharField(pk=True, max_length=128)
    description = fields.TextField(null=True)
    create_time = fields.DatetimeField(auto_now_add=True)
    update_time = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "tb_tag"
        from_attributes = True
        ordering = ["key"]
