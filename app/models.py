from sqlalchemy import Table, Column, String, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from app.database import metadata
import enum
import uuid

class TaskStatus(str, enum.Enum):
    new = "New"
    in_progress = "In Progress"
    completed = "Completed"

users = Table(
    "users",
    metadata,
    Column("username", String(50), primary_key=True, nullable=False),
    Column("first_name", String(50), nullable=False),
    Column("last_name", String(100), nullable=True),
    Column("hashed_password", String(200), nullable=False),
)

tasks = Table(
    "tasks",
    metadata,
    Column("id", UUID(as_uuid=True), primary_key=True, default=lambda: uuid.uuid4()),
    Column("title", String(100), nullable=False),
    Column("description", String(300), nullable=True),
    Column("status", Enum(TaskStatus, native_enum=False), default=TaskStatus.new, nullable=False),
    Column("user_id", String(50), ForeignKey("users.username", ondelete="CASCADE"), nullable=False),
)
