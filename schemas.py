from pydantic import BaseModel, EmailStr
from datetime import datetime

class AllocationCreate(BaseModel):
    asset_name: str
    assigned_to: str

class BookingCreate(BaseModel):
    resource_name: str
    start_time: datetime
    end_time: datetime
    booked_by: str
# --- User Schemas ---
class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    role: str
    is_active: bool

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: str
    password: str

# --- Maintenance Schemas ---
class TicketCreate(BaseModel):
    asset_tag: str
    description: str
    # 'status' ko yahan se hatao agar default model mein set hai, 
    # ya phir yahan optional rakho taaki API confusion na ho.
    
class TicketResponse(TicketCreate):
    id: int
    status: str

    class Config:
        from_attributes = True

# --- Organization Schemas ---
class DepartmentCreate(BaseModel):
    name: str
    head: str
    parent_dept: str = "--"
    status: str = "Active"

class DepartmentResponse(DepartmentCreate):
    id: int

    class Config:
        from_attributes = True

# --- Asset Schemas ---
class AssetCreate(BaseModel):
    name: str
    serial_number: str
    department: str

class TransferCreate(BaseModel):
    asset_tag: str
    to_employee: str
    reason: str


class AllocationCreate(BaseModel):
    asset_name: str
    assigned_to: str

class BookingCreate(BaseModel):
    resource_name: str
    start_time: datetime
    end_time: datetime
    booked_by: str