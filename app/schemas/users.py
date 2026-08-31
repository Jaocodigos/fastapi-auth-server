from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str
    password: str

class UserSelfRegister(BaseModel):
    username: str
    password: str
    email: EmailStr

class UserResponse(BaseModel):
    id: str
    username: str

    class Config:
        from_attributes = True
