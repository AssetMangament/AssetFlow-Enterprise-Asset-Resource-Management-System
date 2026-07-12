from sqlalchemy import Column, Integer, String, DateTime, Text
from database import Base
import datetime

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    role = Column(String, default="employee") 

class Department(Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    head = Column(String, default="N/A")
    parent_dept = Column(String, default="--")
    status = Column(String, default="Active")

class Asset(Base):
    __tablename__ = "assets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String, unique=True, index=True) 
    name = Column(String)
    serial_number = Column(String, unique=True)
    category = Column(String, default="General")
    department = Column(String)
    status = Column(String, default="Available") 
    location = Column(String, default="Main Office")

class Allocation(Base):
    __tablename__ = "allocations"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String)
    assigned_to = Column(String)
    reason = Column(Text)
    date_allocated = Column(DateTime, default=datetime.datetime.utcnow)

class Booking(Base):
    __tablename__ = "bookings"
    id = Column(Integer, primary_key=True, index=True)
    resource_name = Column(String)
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    booked_by = Column(String)

class MaintenanceTicket(Base):
    __tablename__ = "maintenance_tickets"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String)
    description = Column(Text)
    status = Column(String, default="Pending") 
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class AuditRecord(Base):
    __tablename__ = "audit_records"
    id = Column(Integer, primary_key=True, index=True)
    asset_tag = Column(String)
    expected_location = Column(String)
    verification_status = Column(String) 
    audit_date = Column(DateTime, default=datetime.datetime.utcnow)

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String) 
    message = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
