from pydantic import BaseModel, ConfigDict, EmailStr


class UserSchema(BaseModel):
    username: str
    email: EmailStr
    password: str


class responseUserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    model_config = ConfigDict(from_attributes=True)


class UserDB(UserSchema):
    id: int


class UserList(BaseModel):
    users: list[responseUserSchema]


class Token(BaseModel):
    access_token: str
    token_type: str
