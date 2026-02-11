from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import text
from .database import get_db
from .models import Recipe, Ingredient, Instruction, Nutrient
from .schemas import SuggestionRequest, RecipeAvailability
from typing import List
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


@app.get("/instructions")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Instruction).all()


@app.get("/nutrients")
def get_recipes(db: Session = Depends(get_db)):
    return db.query(Nutrient).all()

"""
@app.get("/recipes/nutrition")
def get_nutrition_report(db: Session = Depends(get_db)):
    # You can even use filters or order_by on the view!
    results = db.query(RecipeNutritionView).order_by(RecipeNutritionView.recipe_name.asc()).all()
    return results
"""


@app.post("/recipes/suggestions", response_model=List[RecipeAvailability])
def calculate_recipe_costs(
    request: SuggestionRequest, 
    db: Session = Depends(get_db)
):
    sql = text("""
        SELECT 
            i.recipe AS recipe,
            COUNT(*)                                                                        AS nbr_of_ingredients,
            SUM(
                CASE 
                    WHEN    (quantity * (:portions/ r.portions) ) > quantity_on_stock 
                            OR  CURRENT_DATE > expiration_date::date  
                    THEN 1 
                    ELSE 0 
                END
            )                                                                               AS missing_ingredients,
            SUM(
                CASE 
                    WHEN    expiration_date::date - CURRENT_DATE < :scope 
                            AND expiration_date::date - CURRENT_DATE >= 0 
                    THEN 1 
                    ELSE 0 
                END
            )                                                                               AS "expiring_within_scope", 
            string_agg(
                CASE 
                    WHEN expiration_date::date - CURRENT_DATE < :scope AND expiration_date::date - CURRENT_DATE >= 0 
                    THEN CONCAT(i.ingredient, ' (', i.expiration_date, ') ')
                    ELSE ''
                END, ''
            )                                                                               AS "expiring_ingredients",
            ROUND(SUM(price_per_unit * quantity / r.portions)::numeric, 2)                  AS price_per_portion,
            ROUND(SUM(price_per_unit * quantity * (:portions/ r.portions) )::numeric, 2)    AS price,
            ROUND( 
                SUM(
                    CASE 
                        WHEN    (quantity * (:portions/ r.portions) ) > quantity_on_stock  
                                AND expiration_date::date > CURRENT_DATE
                        THEN ((quantity * (:portions / r.portions) ) - quantity_on_stock) * price_per_unit 
                        ELSE  quantity * (:portions / r.portions) * price_per_unit
                    END
                )::numeric, 2
            )                                                                               AS cost
        FROM recipes r 
        JOIN v_instructions i ON r.name = i.recipe
        GROUP BY i.recipe
        ORDER BY  "expiring_within_scope" desc;
    """)
    
    # execute with the parameter dictionary
    result = db.execute(sql, {"portions": request.portions, "scope": request.scope})
    
    # transform rows into a list of dictionaries for Pydantic to parse
    return [dict(row._mapping) for row in result]