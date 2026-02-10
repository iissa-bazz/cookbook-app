from sqlalchemy import String, Float, ForeignKey, Integer, ForeignKeyConstraint, Date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base
from datetime import datetime



###### BASE MODELS #####

class MenuPlan(Base):
    __tablename__ = "menu_plan"
    # Composite PK: Date and Meal (assuming one entry per meal per day)
    date: Mapped[datetime] = mapped_column(Date, primary_key=True) 
    meal: Mapped[str] = mapped_column(String(200), ForeignKey("recipes.name", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    portions: Mapped[float] = mapped_column(Float)

class Diet(Base):
    __tablename__ = "diets"
    diet: Mapped[str] = mapped_column(String(100), primary_key=True)
    problematic_component: Mapped[str] = mapped_column(String(100), primary_key=True)

class Preference(Base):
    __tablename__ = "preferences"
    # FK to Ingredients name
    article: Mapped[str] = mapped_column(
        String(100), primary_key=True
    )
    problematic_component: Mapped[str] = mapped_column(String(100), primary_key=True)

class Nutrient(Base):
    __tablename__ = "nutrients"
    
    # Primary Key
    ingredient_group: Mapped[str] = mapped_column(String(100), primary_key=True)
    
    # Nutritional values (using Float for all numeric data)
    kcal: Mapped[float] = mapped_column(Float)
    kj: Mapped[float] = mapped_column(Float)
    fat: Mapped[float] = mapped_column(Float)
    saturated_fatty_acids: Mapped[float] = mapped_column(Float)
    mono_unsaturated_fatty_acids: Mapped[float] = mapped_column(Float)
    polyunsaturated_fatty_acids: Mapped[float] = mapped_column(Float)
    cholesterol_mg: Mapped[float] = mapped_column(Float)
    carbohydrates: Mapped[float] = mapped_column(Float)
    sugar: Mapped[float] = mapped_column(Float)
    starch: Mapped[float] = mapped_column(Float)
    dietary_fibre: Mapped[float] = mapped_column(Float)
    protein: Mapped[float] = mapped_column(Float)
    salt: Mapped[float] = mapped_column(Float)

    # Relationship back to ingredients in this group
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="nutrient_info")

class Ingredient(Base):
    __tablename__ = "ingredients"
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    # Foreign Key to Nutrients
    group: Mapped[str] = mapped_column(ForeignKey("nutrients.ingredient_group", ondelete='CASCADE', onupdate='CASCADE'))
    unit: Mapped[str] = mapped_column(String(50), primary_key=True)
    g_per_unit : Mapped[float] = mapped_column(Float)
    price_per_unit : Mapped[float] = mapped_column(Float)
    store: Mapped[str] = mapped_column(String(50))
    quantity_on_stock : Mapped[float] = mapped_column(Float, nullable=False)
    expiration_date: Mapped[datetime] = mapped_column(Date, nullable=True)   
    
    
    # Relationships
    nutrient_info: Mapped["Nutrient"] = relationship(back_populates="ingredients")
    used_in_recipes: Mapped[list["Instruction"]] = relationship(back_populates="ingredient_name")

class Recipe(Base):
    __tablename__ = "recipes"
    name: Mapped[str] = mapped_column(String(200), primary_key=True)
    description: Mapped[str] = mapped_column(String(300))
    portions: Mapped[int] = mapped_column(Integer)

    ingredients_list: Mapped[list["Instruction"]] = relationship(
        back_populates="recipe_name", 
        cascade="all, delete-orphan"
    )

class Instruction(Base):
    __tablename__ = "instructions"
    
    recipe: Mapped[str] = mapped_column(ForeignKey("recipes.name", ondelete='CASCADE', onupdate='CASCADE'), primary_key=True)
    # Note: We remove the individual ForeignKeys from these two lines...
    ingredient: Mapped[str] = mapped_column(String(100), primary_key=True)
    unit: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    quantity: Mapped[float] = mapped_column(Float)
    preparation: Mapped[str] = mapped_column(String(200), nullable=True)

    # ...and define them as a single Constraint here:
    __table_args__ = (
        ForeignKeyConstraint(
            ["ingredient", "unit"],
            ["ingredients.name", "ingredients.unit"],
        ),
    )

    # Relationships
    recipe_name: Mapped["Recipe"] = relationship(back_populates="ingredients_list")
    ingredient_name: Mapped["Ingredient"] = relationship(back_populates="used_in_recipes")
    
    
    
    
    
    
    
    
    
    
    
    ##### VIEW MODELS #####
    
"""    
class InstructionsView(Base):
    __tablename__ = "v_instructions"
    # Views don't have PKs, but SQLAlchemy requires one to track the object.
    # We tell it recipe_name is the unique identifier.
    recipe: Mapped[str] = mapped_column(String, primary_key=True)
    ingredient: Mapped[str] = mapped_column(String, primary_key=True)
    group: Mapped[str] = mapped_column(String)
    unit: Mapped[str] = mapped_column(String, primary_key=True)
    quantity: Mapped[float] = mapped_column(Float)
    preparation: Mapped[str] = mapped_column(String)
    
    total_kcal: Mapped[float] = mapped_column(Float)
    total_protein: Mapped[float] = mapped_column(Float)
    total_fat: Mapped[float] = mapped_column(Float)
    total_carbs: Mapped[float] = mapped_column(Float)
    total_sugar: Mapped[float] = mapped_column(Float)
    total_fiber: Mapped[float] = mapped_column(Float)
"""
    