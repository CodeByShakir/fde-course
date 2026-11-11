from fastapi import FastAPI

app = FastAPI(title="Noor Foods Orders API")


@app.get("/")
def read_root() -> dict[str, str]:
    return {"app": "Noor Foods Orders API", "docs": "/docs"}
