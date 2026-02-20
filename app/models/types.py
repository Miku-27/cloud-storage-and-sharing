from enum import Enum

class FileStatus(str, Enum):
    PENDING = "pending"   
    SUCCESS = "success"   
    FAILED = "failed"     
