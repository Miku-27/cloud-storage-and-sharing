from fastapi import FastAPI
from app.api.file_route import files_route

app = FastAPI()

app.include_router(
    files_route,
    prefix="/file"
)
