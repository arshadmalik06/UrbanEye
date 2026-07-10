from datetime import datetime
from pydantic import BaseModel
class User(BaseModel):
    id:int
    name:str
    email:str
    phone:str
    password:str
    role:str
    created_at:datetime
class UserCreate(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    role:str
class UserUpdate(BaseModel):
    name:str
    email:str
    phone:str
    password:str
    role:str
class UserLogin(BaseModel):
    email:str
    password:str
class UserResponse(BaseModel):
    id:int
    name:str
    email:str
    phone:str
    role:str
    created_at:datetime                     
class Report(BaseModel):
    id:int
    user_id:int
    department_id:int
    title:str
    description:str
    category:str
    image_url:str
    latitude:float
    longitude:float
    address:str
    priority:str
    status:str
    created_at:datetime  
class Status(BaseModel):
    id:int
    report_id:int
    comment:str
    updated_by:str
    timestamp:datetime
class Department(BaseModel):
    id:int
    department_name:str        