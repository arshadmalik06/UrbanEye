from sqlalchemy import Column,Integer,String,Float,DateTime,Text,ForeignKey
from datetime import datetime
from database import Base
class Users(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(100))
    email=Column(String(100))
    phone=Column(String(100))
    password=Column(String(100))
    role=Column(String(100))
    created_at=Column(DateTime,default=datetime.utcnow)
class Reports(Base):
    __tablename__='reports'
    id=Column(Integer,primary_key=True,index=True)
    user_id=Column(Integer,ForeignKey('users.id'))
    department_id=Column(Integer,ForeignKey('departments.id'))
    title=Column(String(100))
    description=Column(Text(300))
    category=Column(String(100))
    image_url=Column(String(100))
    latitude=Column(Float)
    longitude=Column(Float)
    address=Column(String(100))
    priority=Column(String(100))
    status=Column(String(100))
    created_at=Column(DateTime,default=datetime.utcnow)
class Status(Base):
    __tablename__='status'
    id=Column(Integer,primary_key=True,index=True)
    report_id=Column(Integer,ForeignKey('reports.id'))
    comment=Column(String(100))
    updated_by=Column(String(100))
    timestamp=Column(DateTime,default=datetime.utcnow)
class Departments(Base):
    __tablename__='departments'
    id=Column(Integer,primary_key=True,index=True)
    department_name=Column(String(100))
          