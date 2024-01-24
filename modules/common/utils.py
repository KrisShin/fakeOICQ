import random
import string
import time

from config.settings import TIME_NS


def generate_random_id(count: int = 32) -> str:
    """generate random string length in count."""
    if count < TIME_NS:
        return ''.join(random.choices(string.ascii_letters + string.digits, k=count))

    return str(time.time_ns())[:TIME_NS] + ''.join(
        random.choices(string.ascii_lowercase + string.digits, k=count - TIME_NS)
    )


def queryset_to_pydantic_model(queryset, model_class):
    return [model_class.model_validate(item) for item in queryset]
