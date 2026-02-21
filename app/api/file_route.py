from fastapi import APIRouter,Depends
from app.models.schemas import FileCreateModel,FileUpdateModel
from app.models.database import get_db
from app.dependencies import validate_jwt
from app.services.file_service import upload_file_service,update_file,download_file_service
from app.utils.response import make_response

files_router = APIRouter()

@files_router.post("")
def upload_file(file:FileCreateModel,db=Depends(get_db),user_id=Depends(validate_jwt)):
    response = upload_file_service(db,user_id,file.model_dump())
    return make_response(response)

@files_router.patch("/{file_id}")
def confirm_upload(file:FileUpdateModel,file_id:str,db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = update_file(file_id,user_id,db,file.model_dump(exclude_unset=True))
    return make_response(response)

@files_router.get("/{file_id}")
def download_file(file_id:str,db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = download_file_service(file_id,user_id,db) 
    return make_response(response)
