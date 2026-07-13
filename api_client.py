import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
from config import BACKEND_URL
from utils.logger import get_logger

logger = get_logger(__name__)

TIMEOUT = 5


def get_employees():
    try:
        response = requests.get(f"{BACKEND_URL}/employees", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        logger.error(f"Failed to fetch employees from API: {e}")
        return [], str(e)


def create_employee(name, department, salary, hire_date):
    try:
        payload = {
            "name": name,
            "department": department,
            "salary": salary,
            "hire_date": hire_date,
        }
        response = requests.post(f"{BACKEND_URL}/employees", json=payload, timeout=TIMEOUT)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        logger.error(f"Failed to create employee via API: {e}")
        return None, str(e)


def update_employee(employee_id, name, department, salary, hire_date):
    try:
        payload = {
            "name": name,
            "department": department,
            "salary": salary,
            "hire_date": hire_date,
        }
        response = requests.put(
            f"{BACKEND_URL}/employees/{employee_id}", json=payload, timeout=TIMEOUT
        )
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        logger.error(f"Failed to update employee via API: {e}")
        return None, str(e)


def delete_employee(employee_id):
    try:
        response = requests.delete(f"{BACKEND_URL}/employees/{employee_id}", timeout=TIMEOUT)
        response.raise_for_status()
        return response.json(), None
    except Exception as e:
        logger.error(f"Failed to delete employee via API: {e}")
        return None, str(e)
