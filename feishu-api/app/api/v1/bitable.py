from fastapi import APIRouter

router = APIRouter()

@router.get("/fields")
def read_fields():
    return {"message": "Get fields"}