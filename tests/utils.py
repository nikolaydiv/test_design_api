import random
import string
from random import randrange

def random_string(length=8):
    return ''.join(random.choices(string.ascii_lowercase, k=length))

def random_username(k=8):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=k)) + str(random.randint(1000, 9999))

def random_email():
    return f"{random_string(5)}@gmail.com"

def random_password():
    chars = string.ascii_letters + string.digits
    return ''.join(random.choices(chars, k=12))

def random_age():
    return randrange(1, 100)
