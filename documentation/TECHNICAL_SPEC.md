# CookBook Application - Technical Specification

**Version:** 1.0  
**Date:** February 2026  
**Status:** Development - Stage 1 Complete

---

## Executive Summary

CookBook is a full-stack web application designed for comprehensive meal planning, recipe management, and nutritional tracking. The system serves individual households, restaurants, and online food vendors by automating menu planning, inventory management, and shopping list generation while respecting dietary preferences and ingredient expiration dates.

**Current Status:** Database schema implemented with seeding capability. Backend foundation complete.

---

## Table of Contents

1. [System Architecture](#system-architecture)
2. [Database Design](#database-design)
3. [Technology Stack](#technology-stack)
4. [Current Implementation](#current-implementation)
5. [Data Model Details](#data-model-details)
6. [API Design (Planned)](#api-design-planned)
7. [Business Logic](#business-logic)
8. [Security & Constraints](#security--constraints)
9. [Development Roadmap](#development-roadmap)

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend Layer                           │
│  React + TypeScript + Vite + Tanstack Query + Tailwind      │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ REST API (JSON)
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Backend Layer                           │
│     FastAPI + Pydantic Schemas + SQLAlchemy 2.0 ORM         │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ ORM Queries
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                    Persistence Layer                         │
│              PostgreSQL 15 (Dockerized)                      │
│         Composite Keys + Foreign Key Constraints             │
└─────────────────────────────────────────────────────────────┘
```

### Deployment Model (Current)

- **Database:** Containerized PostgreSQL 15 via Docker Compose
- **Backend:** Native Python (FastAPI) - Development mode
- **Frontend:** Native Node.js (Vite dev server) - Infrastructure ready
- **Port Allocation:** PostgreSQL exposed on `5433` (host) to avoid conflicts

---

## Database Design

### Entity-Relationship Overview

The database implements a normalized relational schema with strong referential integrity:

```
Nutrients (1) ──< (N) Ingredients (N,M) ──< (N) MiseEnPlace >── (N) Recipes
                         │                                            │
                         │ (weak FK via name)                         │
                         ▼                                            │
                    Preferences                                       │
                         │                                            │
                         │                                            ▼
                    Diets                                        MenuPlan
```

### Tables

| Table          | Purpose                                    | Key Type            |
|----------------|--------------------------------------------|---------------------|
| `nutrients`    | Nutritional values per ingredient group    | Simple PK           |
| `ingredients`  | Ingredient variations by unit              | Composite PK        |
| `recipes`      | Recipe catalog with serving sizes          | Simple PK           |
| `mise_en_place`| Recipe instructions (ingredient tuples)    | Composite PK + FK   |
| `diets`        | Dietary restrictions mapping               | Composite PK        |
| `preferences`  | User ingredient exclusions                 | Composite PK        |
| `menu_plan`    | Scheduled meals with portions              | Composite PK        |

### Key Design Decisions

#### 1. Composite Primary Keys

**Ingredients Table:**
```sql
PRIMARY KEY (name, unit_default)
```
- **Rationale:** Same ingredient (e.g., "Kiwi") can exist in multiple units ("pieces", "ml", "g")
- **Impact:** Allows flexible inventory tracking per unit variation

**MiseEnPlace Table:**
```sql
PRIMARY KEY (recipe_name, ingredient_name, unit)
FOREIGN KEY (ingredient_name, unit) REFERENCES ingredients(name, unit_default)
```
- **Rationale:** A recipe may use the same ingredient multiple times in different preparations
- **Implementation:** Uses `ForeignKeyConstraint` for composite FK

#### 2. Weak Foreign Key: Preferences → Ingredients

**Problem:** Preferences should reference `ingredients.name` only (not the composite key) because dietary restrictions apply to all unit variations of an ingredient.

**Solution:** Foreign key constraint dropped; enforced via application logic.

**Trade-offs:**
- ✅ Flexibility: "Kiwi" preference applies to all units automatically
- ✅ Simplicity: No need for separate ingredient identity table
- ❌ Risk: Orphaned preferences if ingredients deleted
- ❌ Maintenance: Requires periodic cleanup jobs

**Mitigation Strategy:**
```python
# Application-level validation before insert
def create_preference(session, article, problematic_component):
    if not session.query(Ingredient).filter(Ingredient.name == article).first():
        raise ValueError(f"Ingredient '{article}' does not exist")
    # Proceed with insertion
```

#### 3. Nutrient Grouping

Ingredients link to `nutrients.ingredient_group` for nutritional data aggregation:
- Group: "Milk" → kcal, protein, fat, etc.
- Variations: "Whole Milk", "Skim Milk", "Lactose-Free Milk"
- All variations inherit group-level nutritional profile

---

## Technology Stack

### Backend
- **Framework:** FastAPI 0.104+
- **Language:** Python 3.10+
- **ORM:** SQLAlchemy 2.0 (with `Mapped` annotations)
- **Database Driver:** psycopg2
- **Validation:** Pydantic 2.0
- **Migration Tool:** Alembic (configured, not yet used)

### Frontend (Prepared)
- **Framework:** React 18
- **Language:** TypeScript
- **Build Tool:** Vite
- **State Management:** Tanstack Query (React Query)
- **Styling:** Tailwind CSS
- **HTTP Client:** Axios (planned)

### Infrastructure
- **Database:** PostgreSQL 15
- **Containerization:** Docker + Docker Compose
- **Version Control:** Git
- **Future Deployment:** Docker multi-stage builds for Cloud Run / Firebase

---

## Current Implementation

### Stage 1: Foundation ✅ COMPLETE

#### Database Schema
- 7 tables implemented with full referential integrity
- Composite primary keys working correctly
- Weak FK on Preferences table (application-enforced)

#### Data Seeding
File: `backend/app/seed.py`

**Capabilities:**
- Drops and recreates schema on each run
- Bulk loads data from 7 CSV files:
  - `nutrients.csv` → Nutritional reference data
  - `ingredients.csv` → Ingredient catalog with units
  - `recipes.csv` → Recipe metadata
  - `instructions.csv` → Recipe ingredient lists (Mise en Place)
  - `diets.csv` → Dietary restriction mappings
  - `preferences.csv` → User exclusions
  - `menu_plan.csv` → Scheduled meals

**Usage:**
```bash
python -m app.seed
```

#### Models
File: `backend/app/models.py`

**Key Features:**
- SQLAlchemy 2.0 `Mapped` type annotations
- Bidirectional relationships with `back_populates`
- Cascade delete for `Recipe ← MiseEnPlace`
- Nullable foreign keys for optional data (e.g., `Ingredient.group`)

**Example Model:**
```python
class Recipe(Base):
    __tablename__ = "recipes"
    name: Mapped[str] = mapped_column(String(200), primary_key=True)
    instructions_file: Mapped[str] = mapped_column(String(300))
    portions: Mapped[int] = mapped_column(Integer)
    
    ingredients_list: Mapped[list["MiseEnPlace"]] = relationship(
        back_populates="recipe", 
        cascade="all, delete-orphan"
    )
```

#### Database Configuration
File: `backend/app/database.py`

**Connection String:**
```python
SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost:5433/cookbook"
```

**Session Management:**
```python
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

---

## Data Model Details

### Nutrients Table
Stores nutritional values per 100g of ingredient group.

| Column                        | Type  | Description                      |
|-------------------------------|-------|----------------------------------|
| `ingredient_group` (PK)       | str   | Ingredient category              |
| `kcal`, `kj`                  | float | Energy content                   |
| `graisses`                    | float | Total fats                       |
| `acides_gras_*`               | float | Saturated/mono/polyunsaturated   |
| `cholesterol_mg`              | float | Cholesterol                      |
| `glucides`, `sucres`, `amidon`| float | Carbohydrates breakdown          |
| `fibres_alimentaires`         | float | Dietary fiber                    |
| `proteines`                   | float | Protein content                  |
| `sel`                         | float | Salt content                     |

### Ingredients Table
Catalog of ingredients with unit variations.

| Column              | Type | Description                          |
|---------------------|------|--------------------------------------|
| `name` (PK)         | str  | Ingredient name                      |
| `unit_default` (PK) | str  | Unit of measurement                  |
| `group` (FK)        | str  | Links to `nutrients.ingredient_group`|

**Example Rows:**
```
| name   | unit_default | group |
|--------|--------------|-------|
| Kiwi   | pieces       | Fruit |
| Kiwi   | ml           | Fruit |
| Kiwi   | g            | Fruit |
```

### Recipes Table
Recipe metadata and serving information.

| Column              | Type | Description                      |
|---------------------|------|----------------------------------|
| `name` (PK)         | str  | Recipe name (unique identifier)  |
| `instructions_file` | str  | Path to instruction document     |
| `portions`          | int  | Number of servings               |

### MiseEnPlace Table
The "instruction tuple" linking recipes to ingredients with quantities.

| Column              | Type  | Description                       |
|---------------------|-------|-----------------------------------|
| `recipe_name` (PK, FK) | str | Links to `recipes.name`        |
| `ingredient_name` (PK) | str | Ingredient identifier           |
| `unit` (PK)         | str   | Unit of measurement               |
| `quantity`          | float | Amount needed                     |
| `preparation`       | str   | Prep instructions (nullable)      |

**Composite FK:**
```python
ForeignKeyConstraint(
    ["ingredient_name", "unit"],
    ["ingredients.name", "ingredients.unit_default"]
)
```

### Diets Table
Maps diet types to problematic components.

| Column                     | Type | Description                    |
|----------------------------|------|--------------------------------|
| `diet` (PK)                | str  | Diet name (e.g., "Vegan")      |
| `problematic_component` (PK)| str | Allergen/restriction (e.g., "Lactose") |

**Example:**
```
| diet        | problematic_component |
|-------------|-----------------------|
| Vegan       | Dairy                 |
| Lactose-Free| Lactose               |
| Gluten-Free | Gluten                |
```

### Preferences Table
User exclusions by ingredient and component.

| Column                      | Type | Description                      |
|-----------------------------|------|----------------------------------|
| `article` (PK)              | str  | Ingredient name (weak FK)        |
| `problematic_component` (PK, FK) | str | Links to `diets.problematic_component` |

**Note:** `article` references `ingredients.name` via application logic only.

### MenuPlan Table
Scheduled meals with dates and serving sizes.

| Column         | Type | Description                      |
|----------------|------|----------------------------------|
| `date` (PK)    | str  | Date of meal                     |
| `meal` (PK, FK)| str  | Links to `recipes.name`          |
| `portions`     | int  | Number of servings planned       |

---

## API Design (Planned)

### Stage 2: REST API Layer

#### Pydantic Schemas
Purpose: Prevent circular recursion in JSON serialization.

**Example Schema:**
```python
# schemas.py
from pydantic import BaseModel

class IngredientBase(BaseModel):
    name: str
    unit_default: str
    group: str | None

class MiseEnPlaceResponse(BaseModel):
    ingredient_name: str
    quantity: float
    unit: str
    preparation: str | None
    
    class Config:
        from_attributes = True  # SQLAlchemy 2.0 compatibility

class RecipeResponse(BaseModel):
    name: str
    portions: int
    ingredients_list: list[MiseEnPlaceResponse]
    
    class Config:
        from_attributes = True
```

#### Endpoints (Proposed)

| Method | Endpoint                  | Description                          | Response Schema      |
|--------|---------------------------|--------------------------------------|----------------------|
| GET    | `/recipes`                | List all recipes                     | `List[RecipeBase]`   |
| GET    | `/recipes/{name}`         | Get recipe with ingredients          | `RecipeResponse`     |
| GET    | `/ingredients`            | List all ingredients                 | `List[IngredientBase]`|
| GET    | `/nutrients/{group}`      | Get nutritional info for group       | `NutrientResponse`   |
| GET    | `/menu-plan`              | Get scheduled meals (with filters)   | `List[MenuPlanItem]` |
| POST   | `/menu-plan`              | Add meal to schedule                 | `MenuPlanItem`       |
| GET    | `/shopping-list`          | Generate shopping list               | `ShoppingListResponse`|
| GET    | `/expiring-ingredients`   | Get ingredients near expiration      | `List[ExpiringItem]` |

#### Complex Queries

**Recipe with Full Details:**
```python
@app.get("/recipes/{name}", response_model=RecipeResponse)
async def get_recipe(name: str, db: Session = Depends(get_db)):
    recipe = db.query(Recipe)\
        .options(joinedload(Recipe.ingredients_list))\
        .filter(Recipe.name == name)\
        .first()
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    return recipe
```

**Shopping List Generation:**
- Query: Join `menu_plan` → `recipes` → `mise_en_place` → `ingredients`
- Aggregate quantities by ingredient and unit
- Subtract current inventory (future `on_stock` table)

---

## Business Logic

### Core Features (Planned Implementation)

#### 1. Menu Planning with Dietary Restrictions
**Algorithm:**
```
FOR each preference in user_preferences:
    excluded_ingredients = ingredients WHERE name = preference.article
    FOR each recipe in recipe_catalog:
        IF recipe.ingredients_list INTERSECTS excluded_ingredients:
            mark_recipe_as_incompatible(recipe)
```

**Implementation Location:** Service layer (`backend/app/services/menu_planner.py`)

#### 2. Expiration Date Tracking
**Data Model Addition (Future):**
```python
class OnStock(Base):
    __tablename__ = "on_stock"
    ingredient_name: Mapped[str] = mapped_column(ForeignKey(...), primary_key=True)
    unit: Mapped[str] = mapped_column(primary_key=True)
    quantity: Mapped[float]
    expiration_date: Mapped[date]
    purchase_price: Mapped[float]
```

**Query:**
```sql
SELECT * FROM on_stock
WHERE expiration_date BETWEEN CURRENT_DATE AND CURRENT_DATE + INTERVAL '3 days'
AND NOT EXISTS (
    SELECT 1 FROM menu_plan mp
    JOIN mise_en_place mep ON mp.meal = mep.recipe_name
    WHERE mep.ingredient_name = on_stock.ingredient_name
)
```

#### 3. Shopping List Optimization
**Steps:**
1. Get all ingredients needed for `menu_plan` in date range
2. Aggregate quantities by `(ingredient_name, unit)`
3. Subtract available `on_stock` quantities
4. Group by store/supplier (future enhancement)
5. Calculate total cost

#### 4. Nutritional Summary
**Calculation:**
```python
def calculate_meal_nutrition(recipe_name, portions):
    total_nutrition = defaultdict(float)
    
    for ingredient in recipe.ingredients_list:
        nutrient_data = ingredient.ingredient.nutrient_info
        quantity_factor = ingredient.quantity / 100  # Nutrients are per 100g
        
        for nutrient_field in ['kcal', 'proteines', 'graisses', ...]:
            total_nutrition[nutrient_field] += (
                getattr(nutrient_data, nutrient_field) * quantity_factor
            )
    
    # Normalize per portion
    return {k: v / portions for k, v in total_nutrition.items()}
```

---

## Security & Constraints

### Database Constraints

#### Enforced by PostgreSQL:
- Primary key uniqueness (all tables)
- Foreign key integrity (except `preferences.article`)
- NOT NULL constraints on mandatory fields
- Cascade delete: `Recipe` deletion removes associated `MiseEnPlace` rows

#### Enforced by Application:
- `preferences.article` must exist in `ingredients.name`
- Validation before insert/update operations
- Periodic cleanup job for orphaned preferences

### Data Validation

**SQLAlchemy Level:**
- Type checking via `Mapped` annotations
- String length limits (e.g., `String(100)`)
- Numeric range constraints (implicitly via `Float`, `Integer`)

**Pydantic Level (Future):**
- JSON payload validation
- Field-level validators (e.g., positive quantities)
- Custom business rule validators

### Authentication & Authorization (Future)
- JWT-based authentication
- Role-based access control (RBAC)
  - **Individual:** Full CRUD on own menu plan
  - **Restaurant Manager:** Manage recipes, inventory, menu
  - **Vendor:** Read-only recipe catalog, write orders

---

## Development Roadmap

### ✅ Stage 1: Foundation (COMPLETE)
**Duration:** 2 weeks  
**Deliverables:**
- PostgreSQL Docker setup
- SQLAlchemy 2.0 models with composite keys
- CSV seed script for 7 tables
- Git repository initialization

### 🔄 Stage 2: API & Pydantic Layer (IN PROGRESS)
**Duration:** 2-3 weeks  
**Tasks:**
1. Create Pydantic schemas for all entities
2. Implement `GET /recipes` with pagination
3. Implement `GET /recipes/{name}` with joined loads
4. Implement `GET /ingredients` with filtering
5. Add database session dependency injection
6. Write API endpoint tests (pytest + httpx)

**Acceptance Criteria:**
- All endpoints return valid JSON
- No circular reference errors
- 200ms p95 latency for simple queries
- 500ms p95 latency for complex joins

### 📱 Stage 3: Frontend Foundation
**Duration:** 3 weeks  
**Tasks:**
1. Set up Tanstack Query client configuration
2. Create `RecipeTable` component with Tailwind
3. Implement `RecipeModal` for detailed view
4. Build `Navbar` for navigation
5. Add search/filter on recipe list
6. Implement loading states and error boundaries

**Acceptance Criteria:**
- Functional recipe browsing UI
- Click recipe → modal shows ingredients
- Search filters work client-side
- Mobile-responsive design

### 🧮 Stage 4: Business Logic Implementation
**Duration:** 4 weeks  
**Tasks:**
1. Implement dietary preference filtering service
2. Add `on_stock` table and inventory management
3. Build shopping list aggregation endpoint
4. Create nutritional calculator service
5. Implement expiring ingredient alerts
6. Add meal scheduling logic

**Key Endpoints:**
- `POST /menu-plan` - Schedule meal
- `GET /shopping-list?start_date=X&end_date=Y`
- `GET /nutrition/recipe/{name}`
- `GET /expiring-ingredients?days=3`

### 🐳 Stage 5: Production Deployment
**Duration:** 2 weeks  
**Tasks:**
1. Create multi-stage Dockerfile for backend (Uvicorn)
2. Create Nginx Dockerfile for frontend
3. Configure `nginx.conf` for `/api` reverse proxy
4. Set up Docker Compose for production
5. Configure environment variables (`.env` management)
6. Deploy to Google Cloud Run / Firebase
7. Set up CI/CD pipeline (GitHub Actions)

**Deployment Architecture:**
```
Internet → Load Balancer → Nginx (Frontend + Reverse Proxy)
                             ↓
                          FastAPI Backend
                             ↓
                      Cloud SQL (PostgreSQL)
```

### 🚀 Stage 6: Advanced Features (Future)
**Potential Enhancements:**
- User authentication (Firebase Auth / Auth0)
- Multi-tenancy (restaurant chains, families)
- Recipe sharing and community features
- Barcode scanning for inventory input
- Integration with grocery store APIs
- Meal plan AI recommendations
- Export recipes to PDF
- Nutrition goal tracking (calories, macros)
- Cost optimization algorithms

---

## Performance Considerations

### Database Optimization
- **Indexes:** Add indexes on frequently queried foreign keys
  ```sql
  CREATE INDEX idx_mise_ingredient ON mise_en_place(ingredient_name, unit);
  CREATE INDEX idx_menu_date ON menu_plan(date);
  ```
- **Query Optimization:** Use `joinedload()` for N+1 query prevention
- **Connection Pooling:** SQLAlchemy default pool size (5-10 connections)

### API Optimization
- **Pagination:** Limit recipe lists to 20-50 items per page
- **Caching:** Redis for frequently accessed recipes
- **Response Compression:** Gzip middleware for large JSON payloads

### Frontend Optimization
- **Code Splitting:** Lazy load route components
- **Query Caching:** Tanstack Query 5-minute stale time for static data
- **Image Optimization:** Serve recipe images via CDN

---

## Testing Strategy

### Backend Testing
**Unit Tests:**
- Model methods
- Service layer business logic
- Data validation functions

**Integration Tests:**
- API endpoints with test database
- Database transaction rollback
- Foreign key constraint violations

**Framework:** pytest + pytest-asyncio + httpx

### Frontend Testing
**Component Tests:**
- React component rendering
- User interactions
- State management

**E2E Tests:**
- Critical user flows (recipe selection → menu plan → shopping list)

**Framework:** Vitest + React Testing Library + Playwright

---

## Configuration Management

### Environment Variables

**Backend (`.env`):**
```bash
DATABASE_URL=postgresql://user:password@localhost:5433/cookbook
SECRET_KEY=your-secret-key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (`.env`):**
```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

### Docker Compose Configuration
**Current (`docker-compose.yml`):**
```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: cookbook
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

**Production (Future):**
- Separate services for backend, frontend, database
- Environment-specific overrides (`docker-compose.prod.yml`)
- Secrets management via Docker secrets or Cloud provider

---

## Known Issues & Technical Debt

### Current Issues
1. **No Foreign Key on Preferences:**
   - **Issue:** `preferences.article` → `ingredients.name` enforced by application only
   - **Impact:** Risk of orphaned preferences
   - **Mitigation:** Scheduled cleanup job + validation before insert
   - **Future Fix:** Consider separate `IngredientType` table

2. **No Alembic Migrations:**
   - **Issue:** Schema changes require manual SQL or seed script re-run
   - **Impact:** Difficult to version database schema
   - **Action Item:** Generate initial Alembic migration in Stage 2

3. **Hardcoded Database Credentials:**
   - **Issue:** Credentials in `database.py` and `docker-compose.yml`
   - **Impact:** Security risk if committed to public repo
   - **Action Item:** Move to `.env` files (Stage 2)

4. **No API Authentication:**
   - **Issue:** Endpoints will be publicly accessible
   - **Impact:** Security vulnerability
   - **Action Item:** Implement JWT auth in Stage 4

### Technical Debt
- **Seed Script Drops All Data:** No incremental updates
- **No Logging:** Add structured logging (loguru/structlog)
- **No Monitoring:** Add health check endpoint + metrics (Prometheus)
- **No Input Validation:** Pydantic schemas needed for API
- **No Error Handling:** Custom exception handlers for FastAPI

---

## Appendix A: Sample Queries

### Get Recipe with Ingredients
```python
recipe = session.query(Recipe)\
    .options(
        joinedload(Recipe.ingredients_list)
        .joinedload(MiseEnPlace.ingredient)
        .joinedload(Ingredient.nutrient_info)
    )\
    .filter(Recipe.name == "Pizza Margherita")\
    .first()
```

### Find Recipes Excluding Lactose
```python
excluded_ingredients = session.query(Ingredient.name)\
    .join(Preference, Ingredient.name == Preference.article)\
    .filter(Preference.problematic_component == "Lactose")\
    .all()

safe_recipes = session.query(Recipe)\
    .filter(~Recipe.ingredients_list.any(
        MiseEnPlace.ingredient_name.in_([i[0] for i in excluded_ingredients])
    ))\
    .all()
```

### Calculate Shopping List
```python
from sqlalchemy import func

shopping_list = session.query(
    MiseEnPlace.ingredient_name,
    MiseEnPlace.unit,
    func.sum(MiseEnPlace.quantity * MenuPlan.portions).label("total_quantity")
)\
    .join(MenuPlan, MiseEnPlace.recipe_name == MenuPlan.meal)\
    .filter(MenuPlan.date.between("2023-06-25", "2023-06-30"))\
    .group_by(MiseEnPlace.ingredient_name, MiseEnPlace.unit)\
    .all()
```

---

## Appendix B: File Structure

```
cookbook-app/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI application
│   │   ├── database.py          # SQLAlchemy setup
│   │   ├── models.py            # ORM models
│   │   ├── seed.py              # Data seeding script
│   │   ├── schemas.py           # Pydantic schemas (future)
│   │   ├── routers/             # API endpoints (future)
│   │   │   ├── recipes.py
│   │   │   ├── ingredients.py
│   │   │   └── menu_plan.py
│   │   └── services/            # Business logic (future)
│   │       ├── menu_planner.py
│   │       └── nutrition_calculator.py
│   ├── data/                    # CSV seed data
│   │   ├── nutrients.csv
│   │   ├── ingredients.csv
│   │   ├── recipes.csv
│   │   ├── instructions.csv
│   │   ├── diets.csv
│   │   ├── preferences.csv
│   │   └── menu_plan.csv
│   ├── migrations/              # Alembic migrations
│   ├── tests/                   # Backend tests (future)
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/          # React components (future)
│   │   ├── hooks/               # Custom hooks (future)
│   │   ├── services/            # API clients (future)
│   │   └── main.tsx
│   ├── public/
│   ├── package.json
│   ├── vite.config.ts
│   └── .env.example
├── docker-compose.yml
├── README.md
└── TECHNICAL_SPEC.md
```

---

## Conclusion

The CookBook application foundation is solid with a well-designed relational schema, composite key support, and automated seeding. The next critical steps are implementing the API layer with Pydantic schemas and building the frontend UI. The architecture supports future scalability with clear separation of concerns and a path to production deployment.

**Key Success Factors:**
- Strong database design with referential integrity
- Pragmatic handling of weak FK constraints
- Clear roadmap from prototype to production
- Technology choices aligned with modern best practices

**Next Milestone:** Complete Stage 2 (API layer) within 2-3 weeks to enable frontend integration.
