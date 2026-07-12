from pydantic import BaseModel, EmailStr

# Frontend se jo data aayega (Signup ke time)
class UserCreate(BaseModel):
    name: str
    email: EmailStr  # Ye automatically check karega ki email format sahi hai ya nahi
    password: str

# Backend se jo data wapas jayega (Password hide karke)
class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True # SQLAlchemy models ko Pydantic me convert karne ke liye
class UserLogin(BaseModel):
    email: str
    password: str
class TicketCreate(BaseModel):
    asset_id: str
    description: str
    status: str = "Pending"

class TicketResponse(TicketCreate):
    id: int

    class Config:
        from_attributes = True # ya orm_mode = True
class DepartmentCreate(BaseModel):
    name: str
    head: str
    parent_dept: str = "--"
    status: str = "Active"

class DepartmentResponse(DepartmentCreate):
    id: int

    class Config:
        from_attributes = True