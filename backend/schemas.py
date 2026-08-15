from pydantic import BaseModel, EmailStr
from typing import Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class AdminLogin(BaseModel):
    admin_id: str | int
    password: str

class ProjectCreate(BaseModel):
    name: str
    description: str = ""

class TaskCreate(BaseModel):
    title: str
    status: str = "todo"
    project_id: int
    owner_id: Optional[int] = None

class AdminUserUpdate(BaseModel):
    username: str
    email: EmailStr
    password: Optional[str] = None
    is_admin: bool = False
