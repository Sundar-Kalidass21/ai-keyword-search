from fastapi import FastAPI
from app.core.config import settings
from app.core.logging import logger

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

from app.api.v1.endpoints import search
app.include_router(search.router, prefix=settings.API_V1_STR, tags=["search"])

@app.get("/")
def root():
    return {"message": "Welcome to Hybrid Product Search API"}

@app.get("/health")
def health_check():
    return {"status": "ok"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
