from sqlalchemy import Column,Integer,String,Float,DateTime,Text,ForeignKey
from datetime import datetime
from database import Base
class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(100), nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(100), nullable=False)
    created_at=Column(DateTime,default=datetime.utcnow)
class Reports(Base):
    __tablename__='reports'
    id=Column(Integer,primary_key=True,index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    department_id = Column(Integer, ForeignKey("departments.id"), nullable=True)
    description = Column(Text, nullable=False)
    title=Column(String(100), nullable=False)
    image_url = Column(String(255), nullable=True) 
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String(255), nullable=True, default="")
    category = Column(String(100), nullable=False)
    priority = Column(String(100), nullable=True, default="medium")
    status = Column(String(100), nullable=True, default="submitted")
    created_at=Column(DateTime,default=datetime.utcnow)
class Status(Base):
    __tablename__='status'
    id=Column(Integer,primary_key=True,index=True)
    report_id = Column(Integer, ForeignKey("reports.id"), nullable=False)
    comment = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    timestamp=Column(DateTime,default=datetime.utcnow)
class Departments(Base):
    __tablename__='departments'
    id=Column(Integer,primary_key=True,index=True)
    department_name = Column(String(100), unique=True, nullable=False)
          
