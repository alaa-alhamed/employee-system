import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

from utils import database as db
from utils.logger import get_logger

logger = get_logger(__name__)

app = FastAPI(title="Employee System API", version="1.0.0")


class EmployeeCreate(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    salary: float = Field(..., ge=0)
    hire_date: str


class EmployeeUpdate(BaseModel):
    name: str = Field(..., min_length=1)
    department: str = Field(..., min_length=1)
    salary: float = Field(..., ge=0)
    hire_date: str


class EmployeeOut(BaseModel):
    employee_id: int
    name: str
    department: str
    salary: float
    hire_date: str


@app.on_event("startup")
def on_startup():
    try:
        db.init_db()
        logger.info("Server started successfully and database initialized.")
    except Exception as e:
        logger.error(f"Error during server startup: {e}")
        raise


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/employees", response_model=list[EmployeeOut])
def list_employees():
    try:
        return db.get_all_employees()
    except Exception as e:
        logger.error(f"GET /employees failed: {e}")
        raise HTTPException(status_code=500, detail="Error fetching employees")


@app.get("/employees/{employee_id}", response_model=EmployeeOut)
def get_employee(employee_id: int):
    try:
        employee = db.get_employee_by_id(employee_id)
    except Exception as e:
        logger.error(f"GET /employees/{employee_id} failed: {e}")
        raise HTTPException(status_code=500, detail="Error fetching employee")

    if employee is None:
        raise HTTPException(status_code=404, detail="Employee not found")
    return employee


@app.post("/employees", response_model=EmployeeOut, status_code=201)
def create_employee(employee: EmployeeCreate):
    try:
        new_id = db.create_employee(
            employee.name, employee.department, employee.salary, employee.hire_date
        )
        return db.get_employee_by_id(new_id)
    except Exception as e:
        logger.error(f"POST /employees failed: {e}")
        raise HTTPException(status_code=500, detail="Error creating employee")


@app.put("/employees/{employee_id}", response_model=EmployeeOut)
def update_employee(employee_id: int, employee: EmployeeUpdate):
    try:
        existing = db.get_employee_by_id(employee_id)
        if existing is None:
            raise HTTPException(status_code=404, detail="Employee not found")

        db.update_employee(
            employee_id,
            employee.name,
            employee.department,
            employee.salary,
            employee.hire_date,
        )
        return db.get_employee_by_id(employee_id)
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"PUT /employees/{employee_id} failed: {e}")
        raise HTTPException(status_code=500, detail="Error updating employee")


@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):
    try:
        deleted = db.delete_employee(employee_id)
        if not deleted:
            raise HTTPException(status_code=404, detail="Employee not found")
        return {"message": f"Employee {employee_id} deleted successfully"}
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"DELETE /employees/{employee_id} failed: {e}")
        raise HTTPException(status_code=500, detail="Error deleting employee")
