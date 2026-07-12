from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel

import models
from database import engine, get_db

# THIS is where the magic command belongs!
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class AssetCreate(BaseModel):
    name: str
    serial_number: str
    department: str


@app.get("/api/dashboard")
def get_dashboard_stats(db: Session = Depends(get_db)):
    total_assets = db.query(models.Asset).count()
    allocated_assets = db.query(models.Asset).filter(models.Asset.status == "Allocated").count()
    
    return {
        "available": total_assets - allocated_assets,
        "allocated": allocated_assets
    }

@app.get("/api/assets")
def get_all_assets(db: Session = Depends(get_db)):
    return db.query(models.Asset).all()

@app.post("/api/assets")
def create_asset(asset: AssetCreate, db: Session = Depends(get_db)):
    existing_asset = db.query(models.Asset).filter(models.Asset.serial_number == asset.serial_number).first()
    if existing_asset:
        raise HTTPException(status_code=400, detail="Serial number already registered!")

    asset_count = db.query(models.Asset).count()
    new_tag = f"AF-{asset_count + 100}" 

    new_asset = models.Asset(
        asset_tag=new_tag,
        name=asset.name,
        serial_number=asset.serial_number,
        department=asset.department,
        status="Available"
    )
    db.add(new_asset)
    db.commit()
    
    return {"message": "Asset successfully created!"}
