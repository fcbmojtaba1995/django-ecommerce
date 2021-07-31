import secrets
import string


def generate_password():
    alphabet = string.ascii_letters + string.digits
    password = ''.join(secrets.choice(alphabet) for _ in range(20))
    return password


def generate_username():
    alphabet = string.digits
    username = ''.join(secrets.choice(alphabet) for _ in range(10))
    return 'DK-' + f'{username}'


def generate_verify_code():
    alphabet = string.digits
    verify_code = ''.join(secrets.choice(alphabet) for _ in range(6))
    return str(verify_code)
