from sqlalchemy import Column, Integer, Float, DateTime, JSON
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class Order(Base):
    __tablename__ = "orders"
    
    id = Column(Integer, primary_key=True, index=True)
    products = Column(JSON) 
    total_price = Column(Float)
    created_at = Column(DateTime, default=lambda: datetime.now())