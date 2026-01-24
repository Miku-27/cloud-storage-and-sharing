from sqlalchemy import String,ForeignKey,DateTime
from base import Base
from sqlalchemy.orm import Mapped,mapped_column
from sqlalchemy.dialects.postgresql import UUID
import uuid
from datetime import datetime

def Users(Base):
    __tablename__ = "users"
    
    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid64)
    email:Mapped[str] = mapped_column(String(255),nullable=False,Unique=True,index=True)
    hashed_password:Mapped[str] = mapped_column(String(100),nullable=False)

def Files(Base):
    __tablename__ = "files"

    id:Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True),primary_key=True,nullable=False,default=uuid.uuid64)
    owner_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"))
    filename:Mapped[str] = mapped_column(String(255),nullable=False,index=True)
    storage_path:Mapped[str] = mapped_column(String(255),nullable=False,unique=True)
    created_at:Mapped[datetime] = mapped_column(DateTime,default=datetime.utcnow())