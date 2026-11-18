from fastapi import FastAPI
from sqlmodel import text

from noor_foods_api.database import SessionDep

app = FastAPI(title="Noor Foods API")


@app.get("/")
def root() -> dict[str, str]:
    return {"app": "Noor Foods API", "docs": "/docs"}


@app.get("/health")
def health_check(session: SessionDep) -> dict[str, str | bool]:
    result = session.connection().execute(text("SELECT 1")).scalar()
    return {"status": "ok", "database": result == 1}
