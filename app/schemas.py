from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import datetime
from typing import List, Optional

class BlogBase(BaseModel):
    title: str
    content: str

class BlogCreate(BlogBase):
    pass

class BlogOut(BlogBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: Optional[datetime] = None

    
    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={
            datetime: lambda dt: dt.isoformat()
        }
    )

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str
