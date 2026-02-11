# 🍳 CookBook MVP
**Intelligent Recipe Management & Menu Planning**

A full-stack demo application designed to optimize kitchen management. It suggests recipes based on your current pantry inventory, ingredient expiration dates, and desired portions.

## 🚀 Quick Start

### 1. Prerequisites
* [Docker Desktop](https://www.docker.com/products/docker-desktop/)
* [Git](https://git-scm.com/)

### Initialization & Run
Clone the repository and start the orchestration. This will build the React frontend, FastAPI backend, and initialize the PostgreSQL database.

```bash
git clone https://github.com/iissa-bazz/cookbook.git
cd cookbook
docker compose --profile seed up -d 
```

After the initial build, you can run the application normally with:
```bash
docker compose up -d 
```

### Access the App

- Frontend: http://localhost
- API Documentation (Swagger): http://localhost:8000/docs




## 🛠 Tech Stack

* **Frontend:** React, TypeScript, Vite, TanStack Query, React Router, Axios.
* **Backend:** FastAPI (Python), SQLAlchemy ORM.
* **Infrastructure:** PostgreSQL, Docker, Nginx.

## 💡 Key Features to Explore

1. **Dynamic Suggestions:** On the main page, adjust the "Portions" or "Scope" (days until expiration). The table updates reactively to show the most cost-effective recipes.
2. **Pantry Logic:** The app tracks missing vs. expiring ingredients. Check a recipe's detail view to see exactly what you need.
3. **Error Handling:** The system includes a global Error Boundary and React Query `throwOnError` integration to catch and display API failures gracefully.
