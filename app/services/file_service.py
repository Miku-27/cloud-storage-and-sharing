from app.storage.s3_client import generate_upload_url,generate_download_url
from app.utils.exceptions import ServiceException
from app.utils.response import ResultCodes
from sqlalchemy.exc import SQLAlchemyError
from app.models.model import FilesTable,FileShareTable,FilePermissionTable,UsersTable
from app.services.auth_service import _hash_password
from uuid import UUID
from math import ceil
from app.models.types import FileStatus
from secrets import token_urlsafe
from datetime import datetime,timedelta,timezone

def upload_file_service(db,user_id,file_dict:dict):
    try:

        new_file = FilesTable(
            owner_id = user_id,
            filename = file_dict["file_name"],
            mime_type = file_dict["mime_type"],
            file_size=file_dict["file_size"],
            status=FileStatus.PENDING
        )
        
        db.add(new_file)
        db.flush()
        upload_url = generate_upload_url(new_file.id,new_file.mime_type)
        print(f"url:{upload_url},\n file_key:{new_file.id}")
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

def update_file(file_dict,file_id,db,user_id):
    try:
        file_id = UUID(file_id)
        file = db.query(FilesTable).filter(FilesTable.owner_id == user_id, FilesTable.id == file_id).first()
        if not file:
            raise ServiceException(ResultCodes.FILE_NOT_FOUND)
        
        for key,value in file_dict.items():
            setattr(file,key,value)

        db.commit()
        return {
            "success":True,
            "code":ResultCodes.OPERATION_COMPLETED,
            "data":None
        }
    except SQLAlchemyError as se:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)

def download_file_service(file_id,user_id,db):
    try:
        file_id = UUID(file_id)
        file = db.query(FilesTable).filter(FilesTable.owner_id == user_id, FilesTable.id == file_id).first()
        if not file:
            raise ServiceException(ResultCodes.FILE_NOT_FOUND)
        
        download_url = generate_download_url(file.id,file.filename)

        return {
          "success":True,
          "code":ResultCodes.LINK_GENERATED,
          "data":download_url
        }
    
    except SQLAlchemyError as se:
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)

def delete_file_service(file_id,db,user_id):
    try:
        file_id = UUID(file_id)
        file = db.query(FilesTable).filter(FilesTable.owner_id == user_id and FilesTable.id == file_id).first()
        if not file:
            raise ServiceException(ResultCodes.FILE_NOT_FOUND)
        
        db.delete(file)
        db.commit()
        return {
            "success":True,
            "code":ResultCodes.FILE_DELETED,
            "data":None
        }
    except SQLAlchemyError as se:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)


def generate_share_url_service(link_data_dict,file_id,db,user_id):
    try:
        file_id = UUID(file_id)
        file = db.query(FilesTable).filter(FilesTable.owner_id == user_id and FilesTable.id == file_id).first()
        if not file:
            raise ServiceException(ResultCodes.FILE_NOT_FOUND)
        
        if not link_data_dict['expire_in']:
            link_data_dict['expire_in'] = 604800
        
        if link_data_dict['password']:
            link_data_dict['password'] = _hash_password(link_data_dict['password'])
        
        share_token = token_urlsafe(15)
        now = datetime.now(timezone.utc)
        expires_at = now + timedelta(seconds=link_data_dict['expire_in'])

        share_link_entry = FileShareTable(
            file_id = file_id,
            shared_by = user_id,
            share_token = share_token,
            expires_at = expires_at,
            password_hash = link_data_dict['password']
        )
        db.delete(share_link_entry)
        db.commit()
        return {
            "success":True,
            "code":ResultCodes.LINK_GENERATED,
            "data":share_token
        }
    except SQLAlchemyError as se:
        db.rollback()
        raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR)


scope_map = {
    'owned': lambda stmt,uid:stmt.filter(FilesTable.owner_id == uid),
    'sharedByMe':lambda stmt,uid:stmt.join(FilePermissionTable).filter(FilePermissionTable.granted_by==uid),
    'sharedWithMe':lambda stmt,uid:stmt.join(FilePermissionTable).filter(FilePermissionTable.user_id==uid),   
}
filter_map = {
    "fileName":lambda stmt,filename:stmt.filter(FilesTable.filename.ilike(f"%{filename}%")),
    "mimeType":lambda stmt,type: stmt.filter(FilesTable.mime_type == type ),
    "createdBefore":lambda stmt,date: stmt.filter(FilesTable.created_at <= date ),
    "createdAfter":lambda stmt,date: stmt.filter(FilesTable.created_at >= date ),
    "updatedBefore":lambda stmt,date: stmt.filter(FilesTable.updated_at <= date ),
    "updatedAfter":lambda stmt,date: stmt.filter(FilesTable.updated_at >= date ),
    "sizeLt":lambda stmt,size: stmt.filter(FilesTable.file_size <= size ),
    "sizeGt":lambda stmt,size: stmt.filter(FilesTable.file_size >= size ),
}

def get_user_file_service(db,user_id,filters):
    try:
        page = filters.pop("page",1)
        limit = filters.pop("limit",9)
        offset = (page-1)*limit

        stmt = db.query(FilesTable)
        scope_lambda = scope_map.get(filters.pop('scope'))
        stmt = scope_lambda(stmt,user_id)
        

        for key,value in filters.items():
            lambda_obj = filter_map.get(key)
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
    
def get_users_withfile_access_service(db,file_id,user_id,e_identifier,page=1,limit=3):
    try:

        offset = (page-1)*limit

        stmt = db.query(FilePermissionTable).join(UsersTable).filter(FilePermissionTable.file_id==file_id,FilePermissionTable.granted_by==user_id)
        if e_identifier:
            stmt = stmt.filter(UsersTable.email.ilike(f"%{e_identifier}%"))
        stmt = stmt.order_by(FilePermissionTable.id.desc())
        total_users = stmt.count()
        total_pages = ceil(total_users/limit)

        users = [
            {
                "id":user.id ,
                "name":user.username,
                "email":user.email,
            }
            for (
                user)
                in 
                stmt.limit(limit).offset(offset)
        ]

        users_data = {
            "users":users,
            "page":page,
            "limit":limit,
            "total_page":total_pages,
            "total_file":total_users
        }

        return {
            "success":True,
            "code":ResultCodes.OPERATION_COMPLETED,
            "data":users_data
        }
    
    except SQLAlchemyError as se:
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR) from se
    
def give_permision_service(db,file_id,user_id,access_data):
    try:
        
        permission = db.query(FilePermissionTable).filter(FilePermissionTable.file_id==file_id,FilePermissionTable.granted_by==user_id,FilePermissionTable.user_id==access_data['user_id']).first()
        if permission:
            raise ServiceException(ResultCodes.ACCESS_GRANTED)
        
        new_permission = FilePermissionTable(
            granted_by=user_id,
            user_id=access_data["user_id"],
            file_id=file_id
        )

        db.add(new_permission)
        db.commit()
            
        return {
            "success":True,
            "code":ResultCodes.ACCESS_GRANTED,
            "data":None
        }
    
    except SQLAlchemyError as se:
       db.rollback()
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR) from se
    

def revoke_permision_service(db,file_id,user_id,access_data):
    try:
        
        permission = db.query(FilePermissionTable).filter(FilePermissionTable.file_id==file_id,FilePermissionTable.granted_by==user_id,FilePermissionTable.user_id==access_data['user_id']).first()
        if not permission:
            raise ServiceException(ResultCodes.ACCESS_REVOKED)
        

        db.delete(permission)
        db.commit()
            
        return {
            "success":True,
            "code":ResultCodes.ACCESS_REVOKED,
            "data":None
        }
    
    except SQLAlchemyError as se:
       db.rollback()
       raise ServiceException(ResultCodes.INTERNAL_SERVER_ERROR) from se    