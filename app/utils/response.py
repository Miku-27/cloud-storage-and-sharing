from enum import Enum
from fastapi import status
from fastapi.responses import JSONResponse

class ResultCodes(str, Enum):

    # User Authentication & Registration
    USER_REGISTERED = "USER_REGISTERED"
    USER_ALREADY_EXISTS = "USER_ALREADY_EXISTS"
    USER_NOT_FOUND = "USER_NOT_FOUND"
    
    LOGIN_SUCCESS = "LOGIN_SUCCESS"
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    ACCOUNT_NOT_VERIFIED = "ACCOUNT_NOT_VERIFIED"
    
    PASSWORD_RESET_SENT = "PASSWORD_RESET_SENT"
    PASSWORD_UPDATED = "PASSWORD_UPDATED"

    # File Operations
    FILE_UPLOADED = "FILE_UPLOADED"
    FILE_NOT_FOUND = "FILE_NOT_FOUND"
    FILE_ALREADY_EXISTS = "FILE_ALREADY_EXISTS"
    FILE_DELETED = "FILE_DELETED"
    FILE_RENAMED = "FILE_RENAMED"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    
    # Folder Operations
    FOLDER_CREATED = "FOLDER_CREATED"
    FOLDER_NOT_FOUND = "FOLDER_NOT_FOUND"
    FOLDER_DELETED = "FOLDER_DELETED"
    
    # Sharing & Permissions
    LINK_GENERATED = "LINK_GENERATED"
    PERMISSION_DENIED = "PERMISSION_DENIED"
    ACCESS_GRANTED = "ACCESS_GRANTED"
    ACCESS_REVOKED = "ACCESS_REVOKED"
    SHARE_EXPIRED = "SHARE_EXPIRED"

    # General
    DATA_RETRIEVED = "DATA_RETRIEVED"
    STORAGE_FULL = "STORAGE_FULL"
    OPERATION_COMPLETED = "OPERATION_COMPLETED" 
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR" 

    #JWT
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    TOKEN_INVALID = "TOKEN_INVALID"
    TOKEN_PAYLOAD_INVALID = "TOKEN_PAYLOAD_INVALID"

HTTP_CODE_MAP = {

    "USER_REGISTERED": status.HTTP_201_CREATED,
    "USER_ALREADY_EXISTS": status.HTTP_409_CONFLICT,
    "USER_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    
    "LOGIN_SUCCESS": status.HTTP_200_OK,
    "INVALID_CREDENTIALS": status.HTTP_401_UNAUTHORIZED,
    "ACCOUNT_LOCKED": status.HTTP_403_FORBIDDEN,
    "ACCOUNT_NOT_VERIFIED": status.HTTP_403_FORBIDDEN,
    
    "PASSWORD_RESET_SENT": status.HTTP_200_OK,
    "PASSWORD_UPDATED": status.HTTP_200_OK,

    # File Ops
    "FILE_UPLOADED": status.HTTP_201_CREATED,
    "FILE_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "FILE_ALREADY_EXISTS": status.HTTP_409_CONFLICT,
    "FILE_DELETED": status.HTTP_200_OK,
    "FILE_RENAMED": status.HTTP_200_OK,
    "FILE_TOO_LARGE": status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,

    # Folder Ops
    "FOLDER_CREATED": status.HTTP_201_CREATED,
    "FOLDER_NOT_FOUND": status.HTTP_404_NOT_FOUND,
    "FOLDER_DELETED": status.HTTP_200_OK,

    # Sharing
    "LINK_GENERATED": status.HTTP_201_CREATED,
    "PERMISSION_DENIED": status.HTTP_403_FORBIDDEN,
    "ACCESS_GRANTED": status.HTTP_200_OK,
    "ACCESS_REVOKED": status.HTTP_200_OK,
    "SHARE_EXPIRED": status.HTTP_410_GONE,

    # General
    "DATA_RETRIEVED": status.HTTP_200_OK,
    "STORAGE_FULL": status.HTTP_507_INSUFFICIENT_STORAGE,
    "OPERATION_COMPLETED": status.HTTP_200_OK,
    "INTERNAL_SERVER_ERROR": status.HTTP_500_INTERNAL_SERVER_ERROR,

    #JWT
    "TOKEN_EXPIRED": status.HTTP_401_UNAUTHORIZED,
    "TOKEN_INVALID": status.HTTP_401_UNAUTHORIZED,
    "TOKEN_PAYLOAD_INVALID": status.HTTP_401_UNAUTHORIZED,
}

MESSAGE_MAP = {

    "USER_REGISTERED": "User account created successfully.",
    "USER_ALREADY_EXISTS": "An account with this email or username already exists.",
    "USER_NOT_FOUND": "No user found with the provided identifier.",
    
    "LOGIN_SUCCESS": "Login successful. Welcome back!",
    "INVALID_CREDENTIALS": "The email or password you entered is incorrect.",
    "ACCOUNT_LOCKED": "This account has been locked due to too many failed attempts.",
    "ACCOUNT_NOT_VERIFIED": "Please verify your email address before logging in.",
    
    "PASSWORD_RESET_SENT": "If an account exists, a password reset link has been sent.",
    "PASSWORD_UPDATED": "Your password has been changed successfully.",
    
    "FILE_UPLOADED": "File has been uploaded successfully.",
    "FILE_NOT_FOUND": "The requested file does not exist.",
    "FILE_ALREADY_EXISTS": "A file with this name already exists in this location.",
    "FILE_DELETED": "File successfully moved to trash/deleted.",
    "FILE_RENAMED": "File has been successfully renamed.",
    "FILE_TOO_LARGE": "The file exceeds the maximum allowed upload size.",

    "FOLDER_CREATED": "New folder created successfully.",
    "FOLDER_NOT_FOUND": "The specified folder could not be located.",
    "FOLDER_DELETED": "Folder and its contents have been removed.",

    "LINK_GENERATED": "Public sharing link created successfully.",
    "PERMISSION_DENIED": "You do not have the necessary permissions for this action.",
    "ACCESS_GRANTED": "Access permissions updated successfully.",
    "ACCESS_REVOKED": "User access has been successfully removed.",
    "SHARE_EXPIRED": "The sharing link has expired and is no longer active.",

    "DATA_RETRIEVED": "File/Folder list retrieved successfully.",
    "STORAGE_FULL": "You have reached your storage limit.",
    "OPERATION_COMPLETED": "The requested storage operation was completed.",
    "INTERNAL_SERVER_ERROR": "An unexpected error occurred within the storage service.",

    "TOKEN_EXPIRED": "Your session has expired. Please log in again.",
    "TOKEN_INVALID": "Invalid authentication token. Access denied.",
    "TOKEN_PAYLOAD_INVALID": "The token contains invalid data or claims.",
}

def make_response(service_response):
    success = service_response.get('success')
    code = service_response.get('code')
    data = service_response.get('data', None)

    http_code = HTTP_CODE_MAP.get(code, status.HTTP_500_INTERNAL_SERVER_ERROR)
    msg = MESSAGE_MAP.get(code, "An unknown error occurred.")

    return JSONResponse(
        status_code=http_code,
        content={
            "success": success,
            "msg": msg,
            "data": data,
        }
    )