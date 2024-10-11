from pydantic import BaseModel


class RegisterUserSchemaRequest(BaseModel):
    username: str
    password: str
