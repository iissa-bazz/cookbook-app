from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import get_db
from .models import Recipe, Ingredient, Instruction, Nutrient, RecipeNutritionView
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
    return db.query(Instruction).all()


@app.get("/nutrients")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Nutrient).all()


@app.get("/recipes/nutrition")
def get_nutrition_report(db: Session = Depends(get_db)):
    # You can even use filters or order_by on the view!
    results = db.query(RecipeNutritionView).order_by(RecipeNutritionView.recipe_name.asc()).all()
    return results