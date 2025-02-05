from pydantic import BaseModel


class Login(BaseModel):
    email: str


class LoginInput(BaseModel):
    username: str
    password: str


class LogoutInput(BaseModel):
    user_id: int
