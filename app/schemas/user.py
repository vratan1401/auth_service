from pydantic import BaseModel, EmailStr , ConfigDict
from datetime import datetime
from uuid import UUID

class UserCreate(BaseModel):
    name: str
    phone: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    name: str
    phone: str
    email: EmailStr
    created_time: datetime

    model_config = ConfigDict(
        from_attributes=True,
        json_encoders={UUID: lambda u: str(u)}
    )

