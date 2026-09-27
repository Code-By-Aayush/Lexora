from fastapi import FastAPI
from app.core.config import settings
from app.core.database import Base, engine
from app.api.routes import router

# Create DB Tables automatically if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    description="AI-Powered Judicial Intelligence Platform API"
)

app.include_router(router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}