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
        asset_id=ticket.asset_tag,
        description=ticket.description,
        status=ticket.status
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    return new_ticket
# --- REPORTS & ANALYTICS API ---
@app.get("/api/reports/summary")
def get_reports_summary(db: Session = Depends(get_db)):
    # Future mein ise actual DB se calculate karenge, abhi frontend connect karne ke liye structured data bhej rahe hain
    return {
        "most_used": [
            {"name": "Macbook Pro (AF-0112)", "stat": "booked 18 times"},
            {"name": "Meeting Room 3A", "stat": "45 hrs this month"},
            {"name": "Projector (AF-008)", "stat": "14 uses"}
        ],
        "idle_assets": [
            {"name": "Scanner AF-0021", "stat": "unused 60+ days"},
            {"name": "Chair AF-0418", "stat": "unused 45 days"}
        ]
    }
# --- ORGANIZATION SETUP (DEPARTMENTS) API ---
@app.get("/api/departments", response_model=list[schemas.DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(models.Department).all()

@app.post("/api/departments", response_model=schemas.DepartmentResponse)
def create_department(dept: schemas.DepartmentCreate, db: Session = Depends(get_db)):
    new_dept = models.Department(
        name=dept.name,
        head=dept.head,
        parent_dept=dept.parent_dept,
        status=dept.status
    )
    db.add(new_dept)
    db.commit()
    db.refresh(new_dept)
    return new_dept
@app.post("/api/assets")
def register_asset(asset: schemas.AssetCreate, db: Session = Depends(get_db)):
    # Database me naya asset create karna (Default status: Available)
    new_asset = models.Asset(
        name=asset.name, 
        asset_tag=asset.serial_number, # models.py me humne asset_tag banaya tha
        category=asset.department,     # models.py me humne category banaya tha
        status="Available"
    )
    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)
    return {"message": "Asset registered successfully!", "asset": new_asset}

@app.get("/api/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    # Database se real-time count nikalna
    available_count = db.query(models.Asset).filter(models.Asset.status == "Available").count()
    allocated_count = db.query(models.Asset).filter(models.Asset.status == "Allocated").count()
    
    return {
        "available": available_count,
        "allocated": allocated_count,
        "overdue": 0,
        "active_bookings": 0,
        "pending_transfers": 0,
        "upcoming_returns": 0
    }
@app.get("/api/assets")
def get_all_assets(db: Session = Depends(get_db)):
    # Database se saare assets nikalna
    assets = db.query(models.Asset).all()
    return assets
@app.post("/api/transfers")
def request_transfer(transfer: schemas.TransferCreate, db: Session = Depends(get_db)):
    # 1. Database mein asset ko uske tag (jaise AF-0114) se dhundho
    db_asset = db.query(models.Asset).filter(models.Asset.asset_tag == transfer.asset_tag).first()
    
    # 2. Agar asset na mile toh error do
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset database mein nahi mila")
    
    # 3. Asset ka status update karo
    db_asset.status = "Allocated"
    # (Agar models.py mein 'assigned_to' column hai, toh: db_asset.assigned_to = transfer.to_employee)
    
    # 4. Changes save karo
    db.commit()
    
    return {"message": f"Transfer successful! Asset allocated to {transfer.to_employee}"}
@app.post("/api/maintenance")
def create_maintenance_ticket(ticket: schemas.TicketCreate, db: Session = Depends(get_db)):
    # Yahan sirf ticket.asset_tag use karna hai
    db_asset = db.query(models.Asset).filter(models.Asset.asset_tag == ticket.asset_tag).first()
    
    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset database mein nahi mila")
    
    new_ticket = models.MaintenanceTicket(
        asset_tag=ticket.asset_tag, # Yahan confirm kiya
        description=ticket.description,
        status="Pending"
    )
    db.add(new_ticket)
    db_asset.status = "Maintenance"
    db.commit()
    return {"message": "Maintenance ticket created"}

@app.get("/api/maintenance/tickets")
def get_maintenance_tickets(db: Session = Depends(get_db)):
    tickets = db.query(models.MaintenanceTicket).all()
    result = []
    for t in tickets:
        result.append({
            "asset_id": t.asset_tag, # Frontend yahi field dhund raha hai
            "description": t.description,
            "status": t.status
        })
    return result