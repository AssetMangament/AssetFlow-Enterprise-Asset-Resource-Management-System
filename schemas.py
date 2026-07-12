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