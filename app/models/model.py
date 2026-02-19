from sqlalchemy import String,ForeignKey,DateTime,BigInteger,Integer,Boolean
from app.models.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime,timezone
from app.models.types import FileStatus


#for storing user data
class UsersTable(Base):
    __tablename__ = "users_table"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid4)
    username:Mapped[str] = mapped_column(String(50),nullable=False)
    email:Mapped[str] = mapped_column(String(255),nullable=False,unique=True,index=True)
    hashed_password:Mapped[str] = mapped_column(String(100),nullable=False)


#for storing file data and also the owner of the file /// file could be duplicate here
class FilesTable(Base):
    __tablename__ = "files_table"
    
    # Metadata
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users_table.id",ondelete="CASCADE"))
    filename: Mapped[str] = mapped_column(String(255))
    mime_type :Mapped[str] = mapped_column(String(255),nullable=False)
    # B2 Data
    b2_file_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    status: Mapped[FileStatus] = mapped_column(default=FileStatus.PENDING,nullable=False)
    
    # Stats
    file_size: Mapped[int] = mapped_column(BigInteger, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

#for storing the share url links
class FileShareTable(Base):
    __tablename__ = "file_shares_table"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("files_table.id", ondelete="CASCADE"), nullable=False)
    shared_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users_table.id", ondelete="CASCADE"), nullable=False)

    # We use index=True because we will search by this token every time a link is clicked
    share_token: Mapped[str] = mapped_column(String(100), unique=True, index=True,nullable=False)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    # access_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))


#table for sharing file with peoples
class FilePermissionTable(Base):
    __tablename__="file_permission_table"

    id:Mapped[int]=mapped_column(Integer,primary_key=True,nullable=False,autoincrement=True)
    user_id:Mapped[uuid.UUID] = mapped_column(ForeignKey("users_table.id",ondelete="CASCADE"))
    file_id:Mapped[uuid.UUID]=mapped_column(ForeignKey("files_table.id",ondelete="CASCADE"))
    granted_at:Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now())