from sqlalchemy import Column, Integer, String, Float
from app.configs.database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50))
    description = Column(String(500))
    price = Column(Float)
    quantity = Column(Integer)