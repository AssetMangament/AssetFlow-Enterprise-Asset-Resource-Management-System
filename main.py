from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from database import engine

# Ye line database aur tables (assetflow.db) automatically create karegi
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AssetFlow API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"status": "success", "message": "AssetFlow Backend is running perfectly!"}