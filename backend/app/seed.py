import csv
from sqlalchemy.orm import Session
from .database import engine, Base
from .models import Ingredient, Recipe, MiseEnPlace, Nutrient, Preference, MenuPlan, Diet

def seed_data():
    # Reset Database
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    with Session(engine) as session:
        # Seed Nutrients 
        with open('data/nutrients.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(Nutrient(
                    ingredient_group=row['Ingredient_Group'],
                    kcal=float(row['kcal']),
                    kj=float(row['kJ']),
                    graisses=float(row['graisses']),
                    acides_gras_satures=float(row['acides_gras_satures']),
                    acides_gras_mono_insatures=float(row['acides_gras_mono_insatures']),
                    acides_gras_polyinsatures=float(row['acides_gras_polyinsatures']),
                    cholesterol_mg=float(row['cholesterol_mg']),
                    glucides=float(row['glucides']),
                    sucres=float(row['sucres']),
                    amidon=float(row['amidon']),
                    fibres_alimentaires=float(row['fibres_alimentaires']),
                    proteines=float(row['proteines']),
                    sel=float(row['sel'])
                ))
        session.commit()
        # Seed Ingredients
        with open('data/ingredients.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(Ingredient(
                    name=row['Ingredient'],
                    group=row['Group'],
                    unit_default=row['Unit']
                ))
        
        # Seed Recipes
        with open('data/recipes.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(Recipe(
                    name=row['Nom'],
                    instructions_file=row['Instructions'],
                    portions=int(row['Portions'])
                ))
        
        session.commit() # Commit parents first so foreign keys exist

        # Seed Mise en Place (Instructions)
        with open('data/instructions.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(MiseEnPlace(
                    recipe_name=row['Recipe'],
                    ingredient_name=row['Ingredient'],
                    quantity=float(row['Quantity']),
                    unit=row['Unit'],
                    preparation=row['Preparation']
                ))
        
        session.commit()
        
        # Diets
        with open('data/diets.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(Diet(
                    diet=row['Diet'], # Per your requirement
                    problematic_component=row['Problematic_Component']
                ))
        
        
        # Preferences
        with open('data/preferences.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(Preference(
                    article=row['Ingredient'], # Per your requirement
                    problematic_component=row['Problematic_Component']
                ))
        
        session.commit()
                
                
        # Menu Plan 
        with open('data/menu_plan.csv', newline='', encoding='utf-8') as f:
            for row in csv.DictReader(f):
                session.add(MenuPlan(
                    date=row['Date'],
                    meal=row['Meal'],
                    portions=int(row['Portions'])
                ))
        
        session.commit()
        
        print("Successfully seeded all tables!")

if __name__ == "__main__":
    seed_data()