from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Recipe, Ingredient, MiseEnPlace, Nutrient
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

# Setup CORS so React can talk to us
app.add_middleware(
    CORSMiddleware,
    allow_origins=[os.getenv("CORS_ORIGINS")],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    return {"status": "connected", "database": "PostgreSQL"}


@app.get("/recipes")
def get_recipes(db: Session = Depends(get_db)):
    # Standard query - this will return recipes 
    return db.query(Recipe).all()


@app.get("/ingredients")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Ingredient).all()


@app.get("/mise_en_place")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(MiseEnPlace).all()


@app.get("/nutrients")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Nutrient).all()

