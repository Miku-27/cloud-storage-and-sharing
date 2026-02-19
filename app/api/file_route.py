from fastapi import APIRouter,Depends
from app.models.schemas import FileCreateModel
from app.models.database import get_db
from app.dependencies import validate_jwt
from app.services.file_service import upload_file_service
from app.utils.response import make_response

files_router = APIRouter()

@files_router.post("")
def upload_file(file:FileCreateModel,db=Depends(get_db),user_id=Depends(validate_jwt)):
    response = upload_file_service(db,user_id,file.model_dump())
    return make_response(response)