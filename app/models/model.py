from sqlalchemy import String,ForeignKey,DateTime,BigInteger,Integer,Boolean
from app.models.database import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime,timezone
from app.models.types import FileStatus

class UsersTable(Base):
    __tablename__ = "users_table"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid64)
    email:Mapped[str] = mapped_column(String(255),nullable=False,Unique=True,index=True)
    hashed_password:Mapped[str] = mapped_column(String(100),nullable=False)

class FilesTable(Base):
    __tablename__ = "files_table"
    
    # Metadata
    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    owner_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id"))
    filename: Mapped[str] = mapped_column(String(255))
    
    # B2 Data
    b2_file_id: Mapped[str] = mapped_column(String(255), unique=True, nullable=True)
    status: Mapped[FileStatus] = mapped_column(default=FileStatus.PENDING,nullable=False)
    
    # Stats
    file_size: Mapped[int] = mapped_column(BigInteger, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),server_default=func.now(), onupdate=func.now())

class FileShareTable(Base):
    __tablename__ = "file_shares_table"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    file_id: Mapped[uuid.UUID] = mapped_column(ForeignKey("files.id", ondelete="CASCADE"), nullable=False)
    shared_by: Mapped[uuid.UUID] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    # The random string for the URL (e.g., myapp.com/share/xJ92kLm0)
    # We use index=True because we will search by this token every time a link is clicked
    share_token: Mapped[str] = mapped_column(String(100), unique=True, index=True,nullable=False)
    is_public: Mapped[bool] = mapped_column(Boolean, default=True)
    password_hash: Mapped[str | None] = mapped_column(String(255), nullable=True)
    expires_at: Mapped[datetime | None] = mapped_column(DateTime(timezone=True), nullable=True)
    access_count: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime,default=lambda: datetime.now(timezone.utc))

