import random
import string
from typing import Optional


def generate_random_string(length: int = 30) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))


def generate_random_string_or_none(length: int = 30) -> Optional[str]:
    return None if random.choice([True, False]) else generate_random_string(length)
