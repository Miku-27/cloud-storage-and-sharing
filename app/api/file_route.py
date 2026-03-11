from fastapi import APIRouter,Depends
from app.models.schemas import FileCreateModel,FileUpdateModel,ShareLinkModel,CreateAcessModel
from app.models.database import get_db
from app.dependencies import validate_jwt
from app.services.file_service import upload_file_service,update_file,download_file_service,delete_file_service,generate_share_url_service,get_users_withfile_access_service,give_permision_service
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

@files_router.delete("/{file_id}")
def delete_file(file_id:str,db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = delete_file_service(file_id,user_id,db) 
    return make_response(response)

@files_router.post("/{file_id}/share-link")
def generate_share_url(file_id:str,link_data = ShareLinkModel,db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = generate_share_url_service(link_data.model_dump(),file_id,user_id,db) 
    return make_response(response)

@files_router.get('{file_id}/users')
def get_users_withfile_access(file_id:str,
                              email:str|None=None,
                              page:int=1,
                              limit:int=3,
                              db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = get_users_withfile_access_service(db,file_id,user_id,email,page=1,limit=3)
    return make_response(response)

@files_router.post('{file_id}/users')
def give_userfile_access(file_id:str,
                              access_data:CreateAcessModel,
                              db=Depends(get_db),user_id:str=Depends(validate_jwt)):
    response = give_permision_service(db,file_id,user_id,access_data.model_dump())
    return make_response(response)