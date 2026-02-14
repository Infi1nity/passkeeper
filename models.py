from sqlalchemy import Column, Integer, String, DateTime, Text, ForeignKey
from datetime import datetime
from database import Base
from sqlalchemy.orm import relationship

class Service(Base):
    __tablename__ = 'services'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True, unique=True)
    description = Column(Text, nullable=True)
    passwords = relationship("Password", back_populates='service')

class Password(Base):
    __tablename__ = 'passwords'
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    password = Column(String, nullable=False)
    notes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.now())
    service_id = Column(Integer, ForeignKey('services.id'), nullable=False)
    service = relationship("Service", back_populates='passwords')
    
