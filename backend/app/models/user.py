from sqlalchemy import Column, String, DateTime, Boolean, Integer, Enum
from sqlalchemy.ext.declarative import declarative_base
from datetime import datetime
import uuid
import enum

Base = declarative_base()

class SubscriptionType(str, enum.Enum):
    FREE = "free"
    RESEARCHER = "researcher"
    PROFESSIONAL = "professional"

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    subscription_type = Column(String, default=SubscriptionType.FREE)
    subscription_until = Column(DateTime, nullable=True)
    max_persons = Column(Integer, default=50)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Profile
    avatar_url = Column(String, nullable=True)
    bio = Column(String, nullable=True)
    phone = Column(String, nullable=True)

    # Achievements
    achievements = Column(String, default="[]")  # JSON array
    points = Column(Integer, default=0)
    level = Column(Integer, default=1)

    # Preferences
    public_profile = Column(Boolean, default=False)
    notifications_enabled = Column(Boolean, default=True)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String, index=True)
    action = Column(String)
    resource_type = Column(String)
    resource_id = Column(String)
    changes = Column(String)  # JSON
    ip_address = Column(String)
    user_agent = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)
