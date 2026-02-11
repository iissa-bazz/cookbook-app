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

### Open the browser

You can access the page by navigating to http://localhost