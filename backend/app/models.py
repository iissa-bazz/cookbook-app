from sqlalchemy import String, Float, ForeignKey, Integer, ForeignKeyConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Nutrient(Base):
    __tablename__ = "nutrients"
    
    # Primary Key
    ingredient_group: Mapped[str] = mapped_column(String(100), primary_key=True)
    
    # Nutritional values (using Float for all numeric data)
    kcal: Mapped[float] = mapped_column(Float)
    kj: Mapped[float] = mapped_column(Float)
    graisses: Mapped[float] = mapped_column(Float)
    acides_gras_satures: Mapped[float] = mapped_column(Float)
    acides_gras_mono_insatures: Mapped[float] = mapped_column(Float)
    acides_gras_polyinsatures: Mapped[float] = mapped_column(Float)
    cholesterol_mg: Mapped[float] = mapped_column(Float)
    glucides: Mapped[float] = mapped_column(Float)
    sucres: Mapped[float] = mapped_column(Float)
    amidon: Mapped[float] = mapped_column(Float)
    fibres_alimentaires: Mapped[float] = mapped_column(Float)
    proteines: Mapped[float] = mapped_column(Float)
    sel: Mapped[float] = mapped_column(Float)

    # Relationship back to ingredients in this group
    ingredients: Mapped[list["Ingredient"]] = relationship(back_populates="nutrient_info")

class Ingredient(Base):
    __tablename__ = "ingredients"
    name: Mapped[str] = mapped_column(String(100), primary_key=True)
    unit_default: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    # Foreign Key to Nutrients
    group: Mapped[str] = mapped_column(ForeignKey("nutrients.ingredient_group"), nullable=True)
    
    # Relationships
    nutrient_info: Mapped["Nutrient"] = relationship(back_populates="ingredients")
    used_in_recipes: Mapped[list["MiseEnPlace"]] = relationship(back_populates="ingredient")

class Recipe(Base):
    __tablename__ = "recipes"
    name: Mapped[str] = mapped_column(String(200), primary_key=True)
    instructions_file: Mapped[str] = mapped_column(String(300))
    portions: Mapped[int] = mapped_column(Integer)

    ingredients_list: Mapped[list["MiseEnPlace"]] = relationship(
        back_populates="recipe", 
        cascade="all, delete-orphan"
    )

class MiseEnPlace(Base):
    __tablename__ = "mise_en_place"
    
    recipe_name: Mapped[str] = mapped_column(ForeignKey("recipes.name"), primary_key=True)
    # Note: We remove the individual ForeignKeys from these two lines...
    ingredient_name: Mapped[str] = mapped_column(String(100), primary_key=True)
    unit: Mapped[str] = mapped_column(String(50), primary_key=True)
    
    quantity: Mapped[float] = mapped_column(Float)
    preparation: Mapped[str] = mapped_column(String(200), nullable=True)

    # ...and define them as a single Constraint here:
    __table_args__ = (
        ForeignKeyConstraint(
            ["ingredient_name", "unit"],
            ["ingredients.name", "ingredients.unit_default"],
        ),
    )

    recipe: Mapped["Recipe"] = relationship(back_populates="ingredients_list")
    ingredient: Mapped["Ingredient"] = relationship(back_populates="used_in_recipes")