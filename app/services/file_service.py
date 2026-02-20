from app.storage.s3_client import generate_upload_url
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes
from sqlalchemy.exc import SQLAlchemyError
from app.models.model import FilesTable
from uuid import UUID
from app.models.types import FileStatus

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
        db.commit()
        return {
            "success":True,
            "code":ResultCodes.LINK_GENERATED,
            "data":{
                "upload_url":upload_url,
                "file_key":str(new_file.id)
            }
        }
    except SQLAlchemyError as se:
       db.rollback()
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)

def confirm_upload_service(file_id,db,user_id):
    try:
        file_id = UUID(file_id)
        file = db.query(FilesTable).filter(FilesTable.owner_id == user_id and FilesTable.id == file_id).first()
        if not file:
            raise ServiceException(ResultCodes.FILE_NOT_FOUND)
        
        file(
            status = FileStatus.SUCCESS
        )

        db.commit()
        return {
            "success":True,
            "code":ResultCodes.OPERATION_COMPLETED,
            "data":None
        }
    except SQLAlchemyError as se:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)
