from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
    firstname: str
    lastname: str
    age: int

class User(UserBase):
    id: int

    class Config:
        # Замените orm_mode на from_attributes
        from_attributes = True

class CreateUser(UserBase):
    pass

class UpdateUser(UserBase):
    pass