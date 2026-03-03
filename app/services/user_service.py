from sqlalchemy.exc import SQLAlchemyError
from math import ceil
from app.utils.response import ResultCodes
from app.models.model import FilesTable
from app.utils.exceptions import ServiceException

dynamic_query_map = {
    
}

def get_user_file_service(db,user_id,filters):
    try:
        page = filters.pop("page",1)
        limit = filters.pop("limit",9)
        offset = (page-1)*limit

        stmt = db.query(FilesTable).filter(FilesTable.owner_id == user_id)

        for key,value in filters.items():
            lambda_obj = dynamic_query_map.get(key)
            if lambda_obj:
                stmt = lambda_obj(stmt,value)

        stmt = stmt.order_by(FilesTable.id.desc())
        total_files = stmt.count()
        total_pages = ceil(total_files/limit)

        files = [
            {
                "id":file.id ,
                "name":file.filename,
                "size":file.file_size,
                "type":file.mime_type,
                "updatedAt":file.updated_at
            }
            for (
                file)
                in 
                stmt.limit(limit).offset(offset)
        ]

        book_data = {
            "files":files,
            "page":page,
            "limit":limit,
            "total_page":total_pages,
            "total_file":total_files
        }

        return {
            "success":True,
            "code":ResultCodes.FILE_RETRIVED,
            "data":book_data
        }
    
    except SQLAlchemyError as se:
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR) from se
    