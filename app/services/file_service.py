from app.storage.s3_client import generate_upload_url
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes
from sqlalchemy.exc import SQLAlchemyError
from app.models.model import FilesTable

def upload_file_service(db,user_id,file_dict:dict):
    try:
    
        new_file = FilesTable(
            owner_id = user_id,
            filename = file_dict["file_name"],
            mime_type = file_dict["mime_type"],
            file_size=file_dict["file_size"]
        )
        db.add(new_file)
        db.flush()
        upload_url = generate_upload_url(new_file.id,new_file.mime_type)

        return {
            "success":True,
            "code":ResultCodes.LINK_GENERATED,
            "data":{
                "upload_url":upload_url,
                "file_key":new_file.id
            }
        }
    except SQLAlchemyError as se:
       db.rollback()
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)

        

