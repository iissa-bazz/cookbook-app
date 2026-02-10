from pydantic import BaseModel

class SuggestionRequest(BaseModel):
    portions: float
    scope: int

class RecipeAvailability(BaseModel):
    recipe: str
    nbr_of_ingredients: int
    missing_ingredients: int
    expiring_within_scope: int
    expiring_ingredients: str
    price_per_portion: float
    price: float
    cost: float