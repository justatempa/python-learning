from fastapi import FastAPI

# Import API routers
from app.api.v1 import bitable

app = FastAPI(
    title="Feishu Bitable API",
    description="A FastAPI application for interacting with Feishu Bitable API",
    version="1.0.0",
)

# Include API routers
app.include_router(bitable.router, prefix="/api/v1/bitable", tags=["Bitable"])

@app.get("/")
def read_root():
    return {"Hello": "World"}