from datetime import datetime
from typing import Optional
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
    model_config={
        "from_attributes":True
    }                    
class Report(BaseModel):
    id:int
    user_id:int
    department_id:Optional[int]=None
    title:str
    description:str
    category:str
    image_url:Optional[str]=None
    latitude:float
    longitude:float
    address:Optional[str]=""
    priority:Optional[str]="medium"
    status:Optional[str]="submitted"
    created_at:datetime 
    model_config = {
        "from_attributes": True
    }
class ReportCreate(BaseModel):
    user_id:int
    title:str
    description:str
    category:str
    latitude:float
    longitude:float
    department_id:Optional[int]=None
    image_url:Optional[str]=None
    address:Optional[str]=""
    priority:Optional[str]="medium"
    status:Optional[str]="submitted"
class ReportUpdate(BaseModel):
    title:str
    description:str
    category:str
    image_url:str
    latitude:float
    longitude:float
    address:str
    priority:str
    status:str
class ReportResponse(BaseModel):
    id:int
    user_id:int
    department_id:Optional[int]=None
    title:str
    description:str
    category:str
    image_url:Optional[str]=None
    latitude:float
    longitude:float
    address:Optional[str]=""
    priority:Optional[str]="medium"
    status:Optional[str]="submitted"
    created_at:datetime   
    model_config = {
    "from_attributes": True
}                            
class Status(BaseModel):
    id:int
    report_id:int
    comment:str
    updated_by:str
    timestamp:datetime
    model_config = {
        "from_attributes": True
    }
class StatusCreate(BaseModel):
    report_id:int
    comment:str
    updated_by:str
class StatusUpdate(BaseModel):
    comment:str
    updated_by:str
class StatusResponse(BaseModel):
    id:int
    report_id:int
    comment:str
    updated_by:str
    timestamp:datetime  
    model_config = {
    "from_attributes": True
}      
class Department(BaseModel):
    id:int
    department_name:str
    model_config = {
        "from_attributes": True
    }
class DepartmentCreate(BaseModel):
    department_name:str
class DepartmentUpdate(BaseModel):
    department_name:str
class DepartmentResponse(BaseModel):
    id:int
    department_name:str
    model_config = {
    "from_attributes": True
}
