from fastapi import Depends,FastAPI,HTTPException
from database import engine,Base,session
import models,schemas
from passlib.context import CryptContext
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
app = FastAPI(title="UrbanEye API",description="Citizen Issue Reporting System",version="1.0.0")

from fastapi.middleware.cors import CORSMiddleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return{
        "message":"Welcome to UrbanEye API",
        "status":"Server is running successfully"
    }

def get_db():
    db=session()
    try:
        yield db
    finally:
        db.close()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")        

@app.post("/users",response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user=db.query(models.Users).filter(models.Users.email==user.email).first()
    if existing_user:
        raise HTTPException(status_code=400,detail="Email already registered")
    hashed_password=pwd_context.hash(user.password)
    new_user=models.Users(name=user.name,
                          email=user.email,
                          password=hashed_password,
                          phone=user.phone,
                          role=user.role)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
@app.post("/login",response_model=schemas.UserResponse)
def login_user(login_data: schemas.UserLogin, db: Session = Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.email==login_data.email).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    if not pwd_context.verify(login_data.password, user.password):
        raise HTTPException(status_code=400,detail="Invalid password")
    return user
@app.get("/users/{user_id}",response_model=schemas.UserResponse)
def get_user(user_id:int,db:Session=Depends(get_db)):
    user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if not user:
        raise HTTPException(status_code=404,detail="User not found")
    return user
@app.put("/users/{user_id}",response_model=schemas.UserResponse)
def update_user(user_id:int,user:schemas.UserUpdate,db:Session=Depends(get_db)):
    existing_user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404,detail="User not found")
    existing_user.name=user.name
    existing_user.email=user.email
    existing_user.phone=user.phone
    existing_user.password=pwd_context.hash(user.password)
    existing_user.role=user.role
    db.commit()
    db.refresh(existing_user)
    return existing_user
@app.delete("/users/{user_id}")
def delete_user(user_id:int,db:Session=Depends(get_db)):
    existing_user=db.query(models.Users).filter(models.Users.id==user_id).first()
    if not existing_user:
        raise HTTPException(status_code=404,detail="User not found")
    db.delete(existing_user)
    db.commit()
    return {"message":"User deleted successfully"}
@app.post("/reports",response_model=schemas.ReportResponse)
def create_report(report:schemas.ReportCreate,db:Session=Depends(get_db)):
    new_report=models.Reports(user_id=report.user_id,
                              department_id=report.department_id,
                              title=report.title,
                              description=report.description,
                              category=report.category,
                              image_url=report.image_url,
                              latitude=report.latitude,
                              longitude=report.longitude,
                              address=report.address or "",
                              priority=report.priority or "medium",
                              status=report.status or "submitted")
    db.add(new_report)
    db.commit()
    db.refresh(new_report)
    return new_report
@app.get("/reports/{report_id}",response_model=schemas.Report)
def get_report(report_id:int,db:Session=Depends(get_db)):
    report=db.query(models.Reports).filter(models.Reports.id==report_id).first()
    if not report:
        raise HTTPException(status_code=404,detail="Report not found")
    return report
@app.get("/reports",response_model=list[schemas.Report])
def get_all_reports(db:Session=Depends(get_db)):
    reports=db.query(models.Reports).all()
    return reports
@app.put("/reports/{report_id}",response_model=schemas.Report)
def update_report(report_id:int,report:schemas.ReportUpdate,db:Session=Depends(get_db)):
    existing_report=db.query(models.Reports).filter(models.Reports.id==report_id).first()
    if not existing_report:
        raise HTTPException(status_code=404,detail="Report not found")
    existing_report.title=report.title
    existing_report.description=report.description
    existing_report.category=report.category
    existing_report.image_url=report.image_url
    existing_report.latitude=report.latitude
    existing_report.longitude=report.longitude
    existing_report.address=report.address
    existing_report.priority=report.priority
    existing_report.status=report.status
    db.commit()
    db.refresh(existing_report)
    return existing_report
@app.delete("/reports/{report_id}")
def delete_report(report_id:int,db:Session=Depends(get_db)):
    existing_report=db.query(models.Reports).filter(models.Reports.id==report_id).first()
    if not existing_report:
        raise HTTPException(status_code=404,detail="Report not found")
    db.delete(existing_report)
    db.commit()
    return {"message":"Report deleted successfully"}
@app.post("/status",response_model=schemas.Status)
def create_status(status:schemas.StatusCreate,db:Session=Depends(get_db)):
    new_status=models.Status(report_id=status.report_id,
                             comment=status.comment,
                             updated_by=status.updated_by)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status
@app.get("/status/{status_id}",response_model=schemas.Status)
def get_status(status_id:int,db:Session=Depends(get_db)):
    status=db.query(models.Status).filter(models.Status.id==status_id).first()
    if not status:
        raise HTTPException(status_code=404,detail="Status not found")
    return status
@app.get("/status",response_model=list[schemas.Status])
def get_all_status(db:Session=Depends(get_db)):
    status_list=db.query(models.Status).all()
    return status_list
@app.put("/status/{status_id}",response_model=schemas.Status)
def update_status(status_id:int,status:schemas.StatusUpdate,db:Session=Depends(get_db)):
    existing_status=db.query(models.Status).filter(models.Status.id==status_id).first()
    if not existing_status:
        raise HTTPException(status_code=404,detail="Status not found")
    existing_status.comment=status.comment
    existing_status.updated_by=status.updated_by
    db.commit()
    db.refresh(existing_status)
    return existing_status
@app.delete("/status/{status_id}")
def delete_status(status_id:int,db:Session=Depends(get_db)):
    existing_status=db.query(models.Status).filter(models.Status.id==status_id).first()
    if not existing_status:
        raise HTTPException(status_code=404,detail="Status not found")
    db.delete(existing_status)
    db.commit()
    return {"message":"Status deleted successfully"}
@app.post("/departments",response_model=schemas.Department)
def create_department(department:schemas.DepartmentCreate,db:Session=Depends(get_db)):
    new_department=models.Departments(department_name=department.department_name)
    db.add(new_department)
    db.commit()
    db.refresh(new_department)
    return new_department
@app.get("/departments/{department_id}",response_model=schemas.Department)
def get_department(department_id:int,db:Session=Depends(get_db)):
    department=db.query(models.Departments).filter(models.Departments.id==department_id).first()
    if not department:
        raise HTTPException(status_code=404,detail="Department not found")
    return department
@app.get("/departments",response_model=list[schemas.Department])
def get_all_departments(db:Session=Depends(get_db)):
    departments=db.query(models.Departments).all()
    return departments
@app.put("/departments/{department_id}",response_model=schemas.Department)
def update_department(department_id:int,department:schemas.DepartmentUpdate,db:Session=Depends(get_db)):
    existing_department=db.query(models.Departments).filter(models.Departments.id==department_id).first()
    if not existing_department:
        raise HTTPException(status_code=404,detail="Department not found")
    existing_department.department_name=department.department_name
    db.commit()
    db.refresh(existing_department)
    return existing_department
@app.delete("/departments/{department_id}")
def delete_department(department_id:int,db:Session=Depends(get_db)):
    existing_department=db.query(models.Departments).filter(models.Departments.id==department_id).first()
    if not existing_department:
        raise HTTPException(status_code=404,detail="Department not found")
    db.delete(existing_department)
    db.commit()
    return {"message":"Department deleted successfully"}
@app.get("/admin/dashboard")
def get_admin_dashboard(db:Session=Depends(get_db)):
    total_users=db.query(models.Users).count()
    total_reports=db.query(models.Reports).count()
    total_departments=db.query(models.Departments).count()
    total_status=db.query(models.Status).count()
    pending_reports=db.query(models.Reports).filter(models.Reports.status=="Pending").count()
    in_progress_reports=db.query(models.Reports).filter(models.Reports.status=="In Progress").count()
    resolved_reports=db.query(models.Reports).filter(models.Reports.status=="Resolved").count()
    high_priority_reports=db.query(models.Reports).filter(models.Reports.priority=="High").count()
    today_reports=db.query(models.Reports).filter(models.Reports.created_at>=datetime.utcnow().date()).count()
    return {
        "total_users":total_users,
        "total_reports":total_reports,
        "total_departments":total_departments,
        "total_status":total_status,
        "pending_reports":pending_reports,
        "in_progress_reports":in_progress_reports,
        "resolved_reports":resolved_reports,
        "high_priority_reports":high_priority_reports,
        "today_reports":today_reports
    }
@app.get("/admin/reports")
def get_admin_reports(db:Session=Depends(get_db)):
    reports=db.query(models.Reports).all()
    return reports
@app.get("/admin/reports/{id}")
def get_admin_report(id: int, db: Session = Depends(get_db)):
    report = db.query(models.Reports).filter(models.Reports.id == id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return report
@app.put("/admin/reports/{id}")
def update_admin_report(id: int, report: schemas.Report, db: Session = Depends(get_db)):
    existing_report = db.query(models.Reports).filter(models.Reports.id == id).first()
    if not existing_report:
        raise HTTPException(status_code=404, detail="Report not found")
    existing_report.user_id = report.user_id
    existing_report.department_id = report.department_id
    existing_report.title = report.title
    existing_report.description = report.description
    existing_report.category = report.category
    existing_report.image_url = report.image_url
    existing_report.latitude = report.latitude
    existing_report.longitude = report.longitude
    existing_report.address = report.address
    existing_report.priority = report.priority
    existing_report.status = report.status
    db.commit()
    db.refresh(existing_report)
    return existing_report
@app.delete("/admin/reports/{id}")
def delete_admin_report(id: int, db: Session = Depends(get_db)):
    existing_report = db.query(models.Reports).filter(models.Reports.id == id).first()
    if not existing_report:
        raise HTTPException(status_code=404, detail="Report not found")
    db.delete(existing_report)
    db.commit()
    return {"message": "Report deleted successfully"}
@app.get("/admin/users")
def get_admin_users(db: Session = Depends(get_db)):
    users = db.query(models.Users).all()
    return users
@app.get("/admin/users/{id}")
def get_admin_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
@app.put("/admin/users/{id}")
def update_admin_user(id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    existing_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    existing_user.name = user.name
    existing_user.email = user.email
    existing_user.phone = user.phone
    existing_user.password = pwd_context.hash(user.password)
    existing_user.role = user.role
    db.commit()
    db.refresh(existing_user)
    return existing_user    
@app.delete("/admin/users/{id}")
def delete_admin_user(id: int, db: Session = Depends(get_db)):      
    
    existing_user = db.query(models.Users).filter(models.Users.id == id).first()
    if not existing_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(existing_user)
    db.commit()
    return {"message": "User deleted successfully"}
@app.get("/admin/departments")
def get_admin_departments(db: Session = Depends(get_db)):
    departments = db.query(models.Departments).all()
    return departments
@app.get("/admin/departments/{id}")
def get_admin_department(id: int, db: Session = Depends(get_db)):
    department = db.query(models.Departments).filter(models.Departments.id == id).first()
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    return department
@app.put("/admin/departments/{id}")
def update_admin_department(id: int, department: schemas.Department, db: Session = Depends(get_db)):
    existing_department = db.query(models.Departments).filter(models.Departments.id == id).first()
    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")
    existing_department.department_name = department.department_name
    db.commit()
    db.refresh(existing_department)
    return existing_department
@app.delete("/admin/departments/{id}")
def delete_admin_department(id: int, db: Session = Depends(get_db)):
    existing_department = db.query(models.Departments).filter(models.Departments.id == id).first()
    if not existing_department:
        raise HTTPException(status_code=404, detail="Department not found")
    db.delete(existing_department)
    db.commit()
    return {"message": "Department deleted successfully"}
@app.get("/admin/status")
def get_admin_status(db: Session = Depends(get_db)):
    status = db.query(models.Status).all()
    return status
@app.post("/admin/status", response_model=schemas.Status)
def create_admin_status(status: schemas.Status, db: Session = Depends(get_db)):
    new_status = models.Status(report_id=status.report_id,
                               comment=status.comment,
                               updated_by=status.updated_by)
    db.add(new_status)
    db.commit()
    db.refresh(new_status)
    return new_status
@app.put("/admin/status/{id}", response_model=schemas.Status)   
def update_admin_status(id: int, status: schemas.Status, db: Session = Depends(get_db)):
    existing_status = db.query(models.Status).filter(models.Status.id == id).first()
    if not existing_status:
        raise HTTPException(status_code=404, detail="Status not found")
    existing_status.report_id = status.report_id
    existing_status.comment = status.comment
    existing_status.updated_by = status.updated_by
    db.commit()
    db.refresh(existing_status)
    return existing_status
@app.delete("/admin/status/{id}")
def delete_admin_status(id: int, db: Session = Depends(get_db)):
    existing_status = db.query(models.Status).filter(models.Status.id == id).first()
    if not existing_status:
        raise HTTPException(status_code=404, detail="Status not found")
    db.delete(existing_status)
    db.commit()
    return {"message": "Status deleted successfully"}
@app.put("/admin/reports/{report_id}/status", response_model=schemas.ReportStatusUpdate)
def update_report_status(report_id: int, status_update: schemas.ReportStatusUpdate, db: Session = Depends(get_db)):
    report = db.query(models.Reports).filter(models.Reports.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.status = status_update.status_id
    db.commit()
    db.refresh(report)
    return {"message": "Report status updated successfully"}
@app.put("/admin/reports/{report_id}/priority", response_model=schemas.ReportPriorityUpdate)
def update_report_priority(report_id: int, priority_update: schemas.ReportPriorityUpdate, db: Session = Depends(get_db)):
    report = db.query(models.Reports).filter(models.Reports.id == report_id).first()
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    report.priority = priority_update.priority
    db.commit()
    db.refresh(report)
    return {"message": "Report priority updated successfully"}    
    
    

