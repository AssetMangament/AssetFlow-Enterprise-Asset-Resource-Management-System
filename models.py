from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
from sqlalchemy import Column, Integer, String, Boolean, Float, DateTime
from sqlalchemy.orm import relationship
class Department(Base):
    __tablename__ = "departments"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    is_active = Column(Boolean, default=True)
    
    users = relationship("User", back_populates="department")

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    # Default role Employee set kiya hai (Hackathon Guideline)
    role = Column(String, default="Employee") 
    is_active = Column(Boolean, default=True)
    
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    
    department = relationship("Department", back_populates="users")
class Asset(Base):
    __tablename__ = "assets"
    
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    category = Column(String, nullable=False)
    status = Column(String, default="Available") # Statuses: Available, Allocated, Under Maintenance, etc.
class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"

    id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(String, index=True)  # Example: AF-0062
    description = Column(String)
    status = Column(String, default="Pending") # Pending, Approved, In Progress, Resolved etc.
# --- ASSET ALLOCATION MODEL ---
class Allocation(Base):
    __tablename__ = "allocations"
    id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String, index=True)
    assigned_to = Column(String)
    status = Column(String, default="Active")

# --- RESOURCE BOOKING MODEL ---
class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String, index=True)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    booked_by = Column(String)
class AuditCycle(Base):
    __tablename__ = "audit_cycles"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String) # e.g., "Q2 Audit"
    status = Column(String, default="Open") # Open, Closed