export interface RecipeSuggestion {
  recipe: string;
  nbr_of_ingredients: number;
  missing_ingredients: number;
  expiring_within_scope: number;
  expiring_ingredients: string;
  price_per_portion: number;
  price: number;
  cost: number;
}

export interface SuggestionRequest {
  portions: number;
  scope: number;
}

export interface Instruction {
  id: number;
  recipe: string;
  ingredient: string;
  quantity: number;
  unit: string;
}