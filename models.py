from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from database import Base
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