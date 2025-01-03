from typing import Annotated

from fastapi import Form
from fastapi.security import OAuth2PasswordBearer


class AuthForm:
    def __init__(self,
                 username: Annotated[str, Form],
                 email: Annotated[str, Form],
                 password: Annotated[str, Form],
    ):
        self.username = username
        self.password = password
        self.email = email


auth_schema = OAuth2PasswordBearer(tokenUrl='/get_token')
