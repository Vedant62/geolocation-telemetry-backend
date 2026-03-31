from pydantic import BaseModel, EmailStr, Field, ConfigDict

class UserBase(BaseModel):
    email: EmailStr = Field(..., max_length=50)

class UserCreate(UserBase):
    password: str = Field(..., min_length= 8)

class UserResponse(UserBase):
    model_config = ConfigDict(from_attributes=True)
    id : int

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
