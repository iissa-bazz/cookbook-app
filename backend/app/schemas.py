from pydantic import BaseModel

class PortionRequest(BaseModel):
    requested_portions: int

class RecipeAvailability(BaseModel):
    recipe: str
    price_per_portion: float
    nbr_of_ingredients: int
    price: float
    missing_ingredients: int
    cost: float