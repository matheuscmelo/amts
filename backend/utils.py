from random import choice
from string import ascii_letters, digits

def generate_random_string(length, chars=ascii_letters + digits):
    return ''.join(choice(chars) for _ in range(length))
