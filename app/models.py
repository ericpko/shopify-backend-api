# ------------------------------------------------------------
# SQLAlchemy Database Models
# ------------------------------------------------------------
from email.policy import default
from sqlalchemy import Column, Integer, String, Boolean

from .database import Base


class Item(Base):
    __tablename__ = "inventory"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    quantity = Column(Integer, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    deletion_comments = Column(String, default="", nullable=False)
