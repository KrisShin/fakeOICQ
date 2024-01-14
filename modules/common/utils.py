import random
import string
import time

from modules.config.settings import TIME_NS


def generate_random_id(count: int = 32) -> str:
    """generate random string length in count."""
    if count < TIME_NS:
        return random.choices(string.ascii_lowercase + string.digits, k=count)

    return str(time.time_ns()) + random.choices(
        string.ascii_lowercase + string.digits, k=count - TIME_NS
    )
