import csv
from sqlalchemy.orm import Session
from sqlalchemy import text
from datetime import datetime
from .database import engine, Base
from .models import Ingredient, Recipe, Instruction, Nutrient, Preference, MenuPlan, Diet

def parse_date(date_str):
    if not date_str or date_str.lower() == 'none':
        return None
    return datetime.strptime(date_str, "%Y/%m/%d").date()

def seed_data():
    # Reset Database
    
    with engine.connect() as connection:
        # Use CASCADE to drop the tables AND any views that depend on them
        connection.execute(text("DROP TABLE IF EXISTS recipes, ingredients, instructions, menu_plan, diets, preferences CASCADE;"))
        connection.commit()
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    

    with Session(engine) as session:
        # Seed Nutrients 
        with open('data/nutrients.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Nutrient(
                        ingredient_group=row['Ingredient_Group'],
                        kcal=float(row['kcal']),
                        kj=float(row['kJ']),
                        fat=float(row['graisses']),
                        saturated_fatty_acids=float(row['acides_gras_satures']),
                        mono_unsaturated_fatty_acids=float(row['acides_gras_mono_insatures']),
                        polyunsaturated_fatty_acids=float(row['acides_gras_polyinsatures']),
                        cholesterol_mg=float(row['cholesterol_mg']),
                        carbohydrates=float(row['glucides']),
                        sugar=float(row['sucres']),
                        starch=float(row['amidon']),
                        dietary_fibre=float(row['fibres_alimentaires']),
                        protein=float(row['proteines']),
                        salt=float(row['sel'])
                ))
        session.commit()
        # Seed Ingredients
        with open('data/ingredients.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Ingredient(
                        name=row['Ingredient'],
                        group=row['Group'],
                        unit=row['Unit'],
                        g_per_unit=row['g_Per_Unit'],
                        price_per_unit=row['Price_Per_Unit'],
                        store=row['Store'],
                        quantity_on_stock=row['Quantity_On_Stock'],
                        expiration_date=parse_date(row['Expiration_Date'])
                ))
        
        # Seed Recipes
        with open('data/recipes.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Recipe(
                        name=row['Nom'],
                        description=row['Instructions'],
                        portions=int(row['Portions'])
                ))
        
        session.commit() # Commit parents first so foreign keys exist

        # Seed Mise en Place (Instructions)
        with open('data/instructions.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Instruction(
                        recipe=row['Recipe'],
                        ingredient=row['Ingredient'],
                        quantity=float(row['Quantity']),
                        unit=row['Unit'],
                        preparation=row['Preparation']
                ))
        
        session.commit()
        
        # Diets
        with open('data/diets.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Diet(
                        diet=row['Diet'], # Per your requirement
                        problematic_component=row['Problematic_Component']
                ))
        
        
        # Preferences
        with open('data/preferences.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    Preference(
                        article=row['Ingredient'], # Per your requirement
                        problematic_component=row['Problematic_Component']
                ))
        
        session.commit()
                
                
        # Menu Plan 
        with open('data/menu_plan.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(
                    MenuPlan(
                        date=parse_date(row['Date']),
                        meal=row['Meal'],
                        portions=int(row['Portions'])
                ))
        
        session.commit()
        
        
    with engine.connect() as connection:
        connection.execute(text("""
                                CREATE OR REPLACE VIEW v_instructions AS
                                SELECT 
                                    recipe                                                              AS recipe, 
                                    ingredient                                                          AS ingredient, 
                                    i.unit                                                              AS unit, 
                                    m.quantity                                                          AS quantity,  
                                    quantity * i.g_per_unit                                             AS quantity_in_grams, 
                                    preparation                                                         AS preparation,
                                    ROUND( (quantity * i.price_per_unit)::numeric, 3)                   AS price, 
                                    price_per_unit                                                      AS price_per_unit,
                                    store                                                               AS store,
                                    quantity_on_stock                                                   AS quantity_on_stock,
                                    expiration_date                                                     AS expiration_date
                                FROM instructions m 
                                JOIN ingredients i ON 
                                    i.name = m.ingredient 
                                    AND i.unit = m.unit 
                                ORDER BY recipe    
                                ;
                                """))
        connection.commit()
        
        connection.execute(text("""
                                CREATE OR REPLACE VIEW v_ingredients_nutrition AS
                                SELECT  
                                    name                                                                    AS name,
                                    i.group                                                                 AS group,
                                    unit                                                                    AS unit,
                                    g_per_unit                                                              AS g_per_unit,
                                    price_per_unit                                                          AS price_per_unit,
                                    
                                    ROUND( ((g_per_unit/100)*kcal)::numeric , 4)                            AS unit_kcal,
                                    ROUND( ((g_per_unit/100)*kj)::numeric , 4)                              AS unit_kj,
                                    ROUND( ((g_per_unit/100)*fat)::numeric , 4)                             AS g_per_unit_fat,
                                    ROUND( ((g_per_unit/100)*saturated_fatty_acids)::numeric , 4)           AS g_per_unit_saturated_fatty_acids,
                                    ROUND( ((g_per_unit/100)*mono_unsaturated_fatty_acids)::numeric , 4)    AS g_per_unit_mono_unsaturated_fatty_acids,
                                    ROUND( ((g_per_unit/100)*polyunsaturated_fatty_acids)::numeric , 4)     AS g_per_unit_polyunsaturated_fatty_acids,
                                    ROUND( ((g_per_unit/100)*cholesterol_mg)::numeric , 4)                  AS unit_cholesterol_mg,
                                    ROUND( ((g_per_unit/100)*carbohydrates)::numeric , 4)                   AS g_per_unit_carbohydrates,
                                    ROUND( ((g_per_unit/100)*sugar)::numeric , 4)                           AS g_per_unit_sugar,
                                    ROUND( ((g_per_unit/100)*starch)::numeric , 4)                          AS g_per_unit_starch,
                                    ROUND( ((g_per_unit/100)*dietary_fibre)::numeric , 4)                   AS g_per_unit_dietary_fibre,
                                    ROUND( ((g_per_unit/100)*protein)::numeric , 4)                         AS g_per_unit_protein,
                                    ROUND( ((g_per_unit/100)*salt)::numeric , 4)                            AS g_per_unit_salt
                                    
                                FROM ingredients i 
                                JOIN nutrients n ON  i.group = n.ingredient_group 
                                ORDER BY name;
                                """))
        connection.commit()
        
        connection.execute(text("""
                                CREATE OR REPLACE VIEW v_meal_price_per_portion AS
                                SELECT  
                                    i.recipe        AS recipe,
                                    ROUND(SUM(price_per_unit *quantity/portions)::numeric,2)    AS price_per_portion,
                                    MIN(r.portions )                                            AS default_portions,
                                    COUNT(*)                                                    AS nbr_of_ingredients,
                                    ROUND(SUM(price_per_unit * quantity )::numeric,2)           AS default_price,
                                    SUM(
                                        CASE 
                                            WHEN quantity > quantity_on_stock THEN 1 
                                            ELSE 0 
                                        END
                                    )                                                           AS missing_ingredients,
                                    ROUND( 
                                        SUM(
                                            CASE 
                                                WHEN quantity > quantity_on_stock 
                                                THEN (quantity - quantity_on_stock) * price_per_unit 
                                                ELSE 0 
                                            END
                                        )::numeric, 2
                                    )                                                           AS default_Cost
                                    
                                FROM recipes r 
                                JOIN v_instructions i ON  r.name = i.recipe
                                GROUP BY i.recipe
                                ORDER BY recipe;
                                """))
        connection.commit()
        print("Successfully seeded all tables!")

if __name__ == "__main__":
    seed_data()