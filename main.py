from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext

import models
import schemas
from database import engine, get_db

# Tables create karna
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AssetFlow API")

# CORS setup for Vanilla JS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

# Password hashing setup
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password):
    return pwd_context.hash(password)

# --- SIGNUP API ENDPOINT ---
@app.post("/api/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    # Validation 1: Check karna ki email pehle se exist toh nahi karti
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Password ko hash karna (Security)
    hashed_password = get_password_hash(user.password)
    
    # Naya user banana (Role by default "Employee" jayega models.py se)
    new_user = models.User(
        name=user.name, 
        email=user.email, 
        hashed_password=hashed_password
    )
    
    # Database me save karna
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user