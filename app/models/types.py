from enum import Enum

class FileStatus(str, Enum):
    PENDING = "pending"   # Upload started, not finished
    ACTIVE = "active"     # Success! Ready to share
    FAILED = "failed"     # Upload crashed
    DELETED = "deleted"   # Marked for trash
