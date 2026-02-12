from fastapi import APIRouter,Depends
from app.models.schemas import FileCreateModel
files_router = APIRouter()

@files_router.post("/")
def upload_file(file:FileCreateModel):
    pass