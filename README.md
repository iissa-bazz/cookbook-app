# README
## Overview

CookBook helps individuals, restaurants, and food vendors manage recipes, plan menus, track inventory, and generate shopping lists while respecting dietary preferences and ingredient expiration dates.

### Key Features (Planned)
- **Recipe Catalog** - Store and browse recipes with detailed nutritional information
- **Menu Planning** - Schedule meals with automatic portion scaling
- **Shopping Lists** - Auto-generate shopping lists from menu plans
- **Dietary Filters** - Exclude recipes based on allergies and preferences
- **Expiration Tracking** - Get alerts for ingredients nearing expiration
- **Nutrition Analysis** - Calculate nutritional values per meal and day

### Current Status: Stage 1 Complete 
**Completed:**
- PostgreSQL database schema with 7 tables
- SQLAlchemy 2.0 ORM models with composite keys
- Automated CSV data seeding
- Docker Compose development environment

**Next Milestone:** REST API implementation with Pydantic schemas

---

## Architecture

```
┌──────────────────┐
│  React Frontend  │ ← Stage 3 (Planned)
│  + TanStack Query│
└────────┬─────────┘
         │ REST API
┌────────▼─────────┐
│  FastAPI Backend │ ← Stage 2 (In Progress)
│  + SQLAlchemy 2.0│
└────────┬─────────┘
         │ ORM
┌────────▼─────────┐
│   PostgreSQL 15  │ ← Stage 1 (Complete)
│    (Docker)      │
└──────────────────┘
```

### Technology Stack

**Backend:**
- FastAPI (Python 3.10+)
- SQLAlchemy 2.0 with typed `Mapped` annotations
- Pydantic 2.0 for validation
- psycopg2 database driver
- Alembic for migrations

**Frontend:**
- React 18 + TypeScript
- Vite build tool
- Tanstack Query (React Query) for state management
- Tailwind CSS for styling

**Database:**
- PostgreSQL 15 (Dockerized)
- Composite primary keys for flexible data modeling
- Strong referential integrity with foreign key constraints


---

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Python 3.10 or higher
- Node.js 18+ (for frontend, optional)

### 1. Clone the Repository
```bash
git clone <repository-url>
cd cookbook-app
```

### 2. Start the Database
```bash
docker compose up -d
```
> **Note:** PostgreSQL runs on port `5433` (host) to avoid conflicts with local installations.

Verify the database is running:
```bash
docker ps
# Should show "cookbook_db" container running
```

### 3. Set Up the Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 4. Initialize the Database
This command drops existing tables, recreates the schema, and loads data from CSV files:
```bash
python -m app.seed
```

**Expected Output:**
```
Successfully seeded all tables!
```

**Verify Data:**
```bash
docker exec -it cookbook_db psql -U user -d cookbook -c "SELECT COUNT(*) FROM recipes;"
```

### 5. Start the Development Server (Future)
```bash
uvicorn app.main:app --reload
```
API will be available at: `http://localhost:8000`

### 6. Start the Frontend (Future)
```bash
cd frontend
npm install
npm run dev
```
App will be available at: `http://localhost:5173`

---


##  Database Schema

### Tables Overview

| Table          | Records | Purpose                                    |
|----------------|---------|-------------------------------------------|
| `nutrients`    | ~100    | Nutritional values per ingredient group   |
| `ingredients`  | ~200    | Ingredient catalog with unit variations   |
| `recipes`      | ~50     | Recipe metadata and serving sizes         |
| `mise_en_place`| ~500    | Recipe instructions (ingredient tuples)   |
| `diets`        | ~20     | Dietary restriction mappings              |
| `preferences`  | ~30     | User ingredient exclusions                |
| `menu_plan`    | ~100    | Scheduled meals with portions             |

### Key Relationships

```mermaid
erDiagram
    NUTRIENTS ||--o{ INGREDIENTS : "groups"
    INGREDIENTS ||--o{ MISE_EN_PLACE : "uses"
    RECIPES ||--o{ MISE_EN_PLACE : "contains"
    RECIPES ||--o{ MENU_PLAN : "scheduled in"
    DIETS ||--o{ PREFERENCES : "defines"
    INGREDIENTS }o--|| PREFERENCES : "excluded by"
```

### Notable Design Decisions

**Composite Primary Keys:**
- `ingredients(name, unit_default)` - Same ingredient in different units (e.g., "Kiwi" in pieces, ml, g)
- `mise_en_place(recipe_name, ingredient_name, unit)` - Recipe can use same ingredient multiple times

**Weak Foreign Key:**
- `preferences.article` → `ingredients.name` enforced by application logic, not database
- **Rationale:** Dietary preferences apply to all unit variations of an ingredient
- **Trade-off:** Flexibility vs. strict referential integrity

---


##  Project Structure

```
cookbook-app/
.
├── backend/
│   ├── app/
│   │   ├── database.py       # SQLAlchemy configuration
│   │   ├── main.py           # FastAPI app (Stage 2 )
│   │   ├── models.py         # ORM models (Stage 1 )
│   │   ├── routers/          # API endpoints (Stage 2 )
│   │   ├── schemas.py        # Pydantic schemas (Stage 2 )
│   │   └── seed.py           # CSV data loader (Stage 1 )
│   ├── data/                 # CSV seed files
│   │   ├── diets.csv
│   │   ├── ingredients.csv
│   │   ├── instructions.csv
│   │   ├── menu_plan.csv
│   │   ├── nutrients.csv
│   │   ├── preferences.csv
│   │   └── recipes.csv
│   ├── requirements.txt
│   └── venv
├── documentation/
│   ├── DBModels.pdf
│   ├── DBViewsDependencies.pdf
│   ├── Rapport/
│   │   ├── Diagramme-des-classes.pdf
│   │   ├── Diagramme-des-classes.png
│   │   ├── Rapport.pdf
│   │   ├── Rapport.rmd
│   │   └── Schema_des_relations.png
│   └── TECHNICAL_SPEC.md
├── frontend/
│   ├── src/
│   │   ├── components/          # React components (Stage 3 )
│   │   ├── hooks/               # Custom hooks (Stage 3 )
│   │   └── services/            # API clients (Stage 3 )
│   ├── package.json
│   └── vite.config.ts
├── Demo.ipynb
├── docker-compose.yml           # PostgreSQL container
└── README.md
```


##  Development Roadmap

###  Stage 1: Foundation (Complete)
**Duration:** 2 weeks

**Deliverables:**
- [x] PostgreSQL 15 Docker setup with volume persistence
- [x] SQLAlchemy 2.0 models with composite keys and relationships
- [x] CSV seed script loading 7 tables with ~1000 total records
- [x] Git repository structure

**Key Achievement:** Fully functional relational database with sample data.

---


###  Stage 2: API & Pydantic Layer (In Progress)

#### Tasks
1. **Create Pydantic Schemas** (Week 1)
   - [ ] Define request/response models for all entities
   - [ ] Prevent circular references in Recipe ↔ MiseEnPlace
   - [ ] Add validation rules (positive quantities, non-empty strings)

2. **Implement Core Endpoints** (Week 1-2)
   - [ ] `GET /recipes` - List recipes with pagination
   - [ ] `GET /recipes/{name}` - Get recipe with ingredients (joined load)
   - [ ] `GET /ingredients` - List ingredients with filtering
   - [ ] `GET /nutrients/{group}` - Get nutritional info

3. **Database Session Management** (Week 2)
   - [ ] Create FastAPI dependency for session injection
   - [ ] Implement automatic session cleanup
   - [ ] Add error handling for database exceptions

4. **Testing** (Week 2-3)
   - [ ] Write pytest tests for endpoints
   - [ ] Test composite key constraints
   - [ ] Validate Pydantic schema serialization

#### Example Endpoint Implementation
```python
# app/routers/recipes.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, joinedload
from ..schemas import RecipeResponse
from ..models import Recipe
from ..database import get_db

router = APIRouter(prefix="/recipes", tags=["recipes"])

@router.get("/{name}", response_model=RecipeResponse)
async def get_recipe(name: str, db: Session = Depends(get_db)):
    recipe = db.query(Recipe)\
        .options(joinedload(Recipe.ingredients_list))\
        .filter(Recipe.name == name)\
        .first()
    
    if not recipe:
        raise HTTPException(status_code=404, detail="Recipe not found")
    
    return recipe
```

#### Acceptance Criteria
-  All endpoints return valid JSON without circular references
-  P95 latency < 200ms for simple queries, < 500ms for complex joins
-  100% endpoint test coverage
-  API documentation auto-generated at `/docs`

---

### 📱 Stage 3: Frontend Foundation
**Duration:** 3 weeks  
**Prerequisites:** Stage 2 complete

#### Tasks
1. **Setup** (Week 1)
   - [ ] Configure Tanstack Query client
   - [ ] Set up Axios with base URL
   - [ ] Create reusable API hooks

2. **Components** (Week 1-2)
   - [ ] `RecipeTable` - Paginated recipe list with Tailwind
   - [ ] `RecipeModal` - Show ingredients and instructions
   - [ ] `Navbar` - Navigate between Recipes/Ingredients/Menu Plan
   - [ ] `SearchBar` - Filter recipes client-side

3. **State Management** (Week 2)
   - [ ] Implement Tanstack Query for recipe fetching
   - [ ] Add loading/error states
   - [ ] Implement optimistic updates for menu planning

4. **Styling** (Week 3)
   - [ ] Mobile-responsive design
   - [ ] Dark mode support
   - [ ] Accessibility (ARIA labels, keyboard navigation)



#### Acceptance Criteria
-  Users can browse and search recipes
-  Modal displays full recipe details on click
-  App is mobile-responsive
-  No layout shifts during loading

---


---

###  Stage 4: Business Logic Implementation
**Duration:** 4 weeks  
**Prerequisites:** Stage 3 complete

#### Key Features

**1. Menu Planning with Dietary Filters**
**2. Grocery List Generation**
**3. Nutritional Calculator**
**4. Expiration Alerts** (Requires `on_stock` table)

#### New Endpoints
- `GET /menu-plan/compatible?preferences=Lactose,Gluten`
- `GET /shopping-list?start=2023-06-25&end=2023-06-30`
- `GET /nutrition/recipe/{name}`
- `GET /nutrition/day/{date}`
- `GET /inventory/expiring?days=3`

#### Acceptance Criteria
-  Dietary filters correctly exclude incompatible recipes
-  Grocery lists aggregate quantities correctly
-  Nutritional values accurate to ±5%
-  Expiration alerts trigger at correct times

---

###  Stage 5: Production Deployment
**Duration:** 2 weeks  
**Prerequisites:** Stage 4 complete

#### Tasks

**1. Dockerize Backend**

```dockerfile
# backend/Dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**2. Dockerize Frontend**

```dockerfile
# frontend/Dockerfile
# Build stage
FROM node:18 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Production stage
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf
```

**3. Nginx Configuration**

```nginx
# frontend/nginx.conf
server {
    listen 80;
    root /usr/share/nginx/html;
    
    location / {
        try_files $uri $uri/ /index.html;
    }
    
    location /api {
        proxy_pass http://backend:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**4. Production Docker Compose**

```yaml
# docker-compose.prod.yml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_USER: ${DB_USER}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: cookbook
    volumes:
      - postgres_data:/var/lib/postgresql/data

  backend:
    build: ./backend
    environment:
      DATABASE_URL: postgresql://${DB_USER}:${DB_PASSWORD}@db:5432/cookbook
    depends_on:
      - db

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
```

**5. CI/CD Pipeline** (GitHub Actions)

```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud Run
on:
  push:
    branches: [main]
jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Build and push Docker images
        # ... build steps
      - name: Deploy to Cloud Run
        # ... deployment steps
```

#### Deployment Options
- **Google Cloud Run** (Recommended)
  - Automatic scaling
  - Pay-per-use pricing
  - Managed SSL certificates

- **Firebase Hosting + Cloud Run**
  - Static frontend on Firebase CDN
  - Backend on Cloud Run
  - Integrated authentication

- **DigitalOcean App Platform**
  - Simple deployment from GitHub
  - Managed database option
  - Built-in monitoring



#### Acceptance Criteria
-  App accessible via public URL with SSL
-  Database migrations automated
-  Environment variables managed securely
-  CI/CD pipeline deploys on push to main
-  Health check endpoint returns 200

---

##  Environment Variables

### Backend `.env`
```bash
# Database
DATABASE_URL=postgresql://user:password@localhost:5433/cookbook

# Security
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend `.env`
```bash
VITE_API_BASE_URL=http://localhost:8000/api
```

> **Important:** Never commit `.env` files to version control. Use `.env.example` as a template.

---

##  Testing

### Run Backend Tests
```bash
cd backend
pytest tests/ -v
```

### Run Frontend Tests
```bash
cd frontend
npm run test
```

### End-to-End Tests
```bash
npm run test:e2e
```