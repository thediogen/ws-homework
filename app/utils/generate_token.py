import random


def generate_token() -> int:
    '''
    Generates token for user to add to request.session
    '''

    token = random.randint(100000, 999999)

    return token