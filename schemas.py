from pydantic import BaseModel
from datetime import datetime

class ServiceBase(BaseModel):
    name: str
    description: str

class ServiceCreate(ServiceBase):
    pass

class ServiceResponse(ServiceBase):
    id: int

    class Config:
        from_attributes = True


class PasswordBase(BaseModel):
    username: str
    password: str
    notes: str
    service_id: int

class PasswordCreate(PasswordBase):
    pass

class PasswordResponse(PasswordBase):
    id: int
    created_at: datetime
    
    class Config:
        from_attributes = True

class ServiceWithPasswords(ServiceResponse):
    passwords: list[PasswordResponse]