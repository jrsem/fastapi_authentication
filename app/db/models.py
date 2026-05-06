from sqlalchemy import Column, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import relationship
import uuid
from sqlalchemy.dialects.postgresql import UUID, ENUM
from datetime import datetime, timezone
from app.db.dependencies import Base
import enum


class RolesEnum(enum.Enum):
    USER = "USER"
    PROFESSEUR = "PROFESSEUR"
    DECANAT = "DECANAT"


class User(Base):
    __tablename__ = "users"

    id = Column("id", UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column("name", String, nullable=False, index=True)
    username = Column("username", String, nullable=False, index=True)
    password = Column("password", String)
    phone = Column("phone", String)
    active = Column("active", Boolean)
    admin = Column("admin", Boolean, default=False)
    role = Column("role", ENUM(RolesEnum), default=RolesEnum.USER, nullable=False)
    created_at = Column("created_at", DateTime, default=datetime.now(timezone.utc))

    def __init__(self, name, username, phone, role, password, active=True, admin=False):
        self.name = name
        self.password = password
        self.active = active
        self.phone = phone
        self.username = username
        self.admin = admin
        self.role = role
