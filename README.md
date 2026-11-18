# Forward Deployed Engineer (FDE) Program — Coursework & Projects

**Student:** Shakir Aziz  
**Program:** Edversity Forward Deployed Engineer Training Program (2026)

This repository tracks my weekly assignments, exercises, and backend engineering builds as I transition from full-stack web development (Next.js, React, TypeScript, Node.js) into AI Engineering.

## Repository Structure & Progress

| Week       | Module                      | Key Technologies                                | Projects & Deliverables                                                                                                                                         | Status      |
| :--------- | :-------------------------- | :---------------------------------------------- | :-------------------------------------------------------------------------------------------------------------------------------------------------------------- | :---------- |
| **Week 1** | Python & Developer Toolkit  | Python, JSON, Git, GitHub                       | **Café Expense Report:** CLI script parsing `expenses.json`, computing dynamic category totals, flagging high expenses, and generating `summary.json`.          | Completed   |
| **Week 2** | Python for Real Work        | `uv`, `ruff`, `mypy`, Pydantic, Enums, `pytest` | Type-safe Python modules, runtime schema validation models, and automated unit testing suites.                                                                  | Completed   |
| **Week 3** | The Web, APIs & Databases   | FastAPI, Pydantic, `TestClient`, Bruno, Docker  | **Noor Foods Products API:** In-memory REST CRUD API with query filtering, `409` stock conflict protection, 15+ `pytest` tests, and a Bruno collection.         | Completed   |
| **Week 4** | APIs & Relational Databases | PostgreSQL, SQL, SQLModel, Alembic              | **Noor Foods Database & Backend:** Relational schema design, complex SQL queries (`WHERE`, `GROUP BY`, `HAVING`, `JOIN`), and FastAPI + PostgreSQL integration. | In Progress |

## Tech Stack & Local Environment

- **Language & Runtime:** Python 3.12+, managed with `uv`
- **API & Validation:** FastAPI, Pydantic, SQLModel
- **Database & Containers:** PostgreSQL 18, Docker Desktop, DBeaver
- **Testing & Quality:** `pytest`, `ruff`, `mypy`, Bruno

## Running Projects Locally

1. Navigate to the target project directory (e.g., `products-api`):
   ```bash
   cd products-api
   ```
