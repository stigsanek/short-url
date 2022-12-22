import random
import string


def generate_uid(size: int = 10) -> str:
    """Generate random uid"""
    chars = string.ascii_uppercase + string.ascii_lowercase + string.digits
    return ''.join(random.SystemRandom().choice(chars) for _ in range(size))
