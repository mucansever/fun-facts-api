from fastapi import FastAPI
import uvicorn

from app.adapter.api.v1 import router as fun_fact_router


def create_app() -> FastAPI:
    app = FastAPI(title="Daily Fun Fact API")
    app.include_router(fun_fact_router, tags=["fun facts"])
    return app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True, workers=3)
