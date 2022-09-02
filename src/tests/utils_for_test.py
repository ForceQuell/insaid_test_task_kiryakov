import random
import string
from typing import Optional


def generate_random_string(length: int = 30) -> str:
    return "".join(random.choice(string.ascii_letters) for _ in range(length))
