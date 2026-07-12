from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from pydantic import BaseModel # Naya add kiya login schema ke liye
import models
import schemas
from database import engine, get_db

# Login ke liye Pydantic Schema (Taaki error na aaye)
class UserLogin(BaseModel):
    email: str
    password: str

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

@app.get("/api/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Database se real-time count nikalna
    available_count = db.query(models.Asset).filter(models.Asset.status == "Available").count()
    allocated_count = db.query(models.Asset).filter(models.Asset.status == "Allocated").count()
    
    # Baaki metrics abhi 0 bhej rahe hain, jab unke tables banenge tab inko bhi dynamic kar denge
    return {
        "available": available_count,
        "allocated": allocated_count,
        "overdue": 0,
        "active_bookings": 0,
        "pending_transfers": 0,
        "upcoming_returns": 0
    }

@app.get("/")
def read_root():
    return {"status": "success", "message": "AssetFlow API is working!"}

# --- LOGIN API ENDPOINT (Updated) ---
@app.post("/auth/login")
def login_user(user: UserLogin, db: Session = Depends(get_db)):
    # 1. Database mein user ko email se dhoondna (models.User fix kiya)
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email registered nahi hai. Kripya signup karein."
        )
    
    # 2. Password verify karna
    if not pwd_context.verify(user.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Galat password. Kripya fir se koshish karein."
        )
    
    # 3. Successful login par response bhejna
    return {
        "status": "success",
        "message": "Login successful",
        "user": {"id": db_user.id, "name": db_user.name, "email": db_user.email}
    }
# --- MAINTENANCE API ---
@app.get("/api/maintenance/tickets", response_model=list[schemas.TicketResponse])
def get_tickets(db: Session = Depends(get_db)):
    return db.query(models.MaintenanceTicket).all()

@app.post("/api/maintenance/tickets", response_model=schemas.TicketResponse)
def create_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    new_ticket = models.MaintenanceTicket(
        asset_id=ticket.asset_id,
        description=ticket.description,
        status=ticket.status
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket