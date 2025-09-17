from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.configs.database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    role = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role")
