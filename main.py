from fastapi import Depends,FastAPI
from database import engine,Base,session
import models
from sqlalchemy.orm import Session
Base.metadata.create_all(bind=engine)
app = FastAPI(title="UrbanEye API",description="Citizen Issue Reporting System",version="1.0.0")
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

@app.post("/users")
def create_user(user:models.Users, db: Session = Depends(get_db)):
    db.add(user)
    db.commit()
    db.refresh(user)
    db.close()
    return user



