from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

import models
import schemas

from database import engine, SessionLocal, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Employee Management System"
)

# Database connection
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# 1. Home API
@app.get("/")
def home():
    return {"message": "Welcome to Employee Management System"}


# 2. Add employee
@app.post("/employees/")
def add_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    new_employee = models.Employee(**employee.model_dump())

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# 3. View all employees
@app.get("/employees/")
def get_employees(db: Session = Depends(get_db)):
    return db.query(models.Employee).all()


# 4. View one employee
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    return employee


# 5. Update employee
@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    updated_data: schemas.EmployeeCreate,
    db: Session = Depends(get_db)
):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    for key, value in updated_data.model_dump().items():
        setattr(employee, key, value)

    db.commit()
    db.refresh(employee)

    return employee


# 6. Delete employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int, db: Session = Depends(get_db)):
    employee = db.query(models.Employee).filter(
        models.Employee.id == employee_id
    ).first()

    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")

    db.delete(employee)
    db.commit()

    return {"message": "Employee deleted successfully"}