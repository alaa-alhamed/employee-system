import sqlite3
import os
from typing import Optional

from config import DB_PATH, SQL_INIT_PATH
from utils.logger import get_logger

logger = get_logger(__name__)


def get_connection() -> sqlite3.Connection:
    try:
        os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise


def init_db() -> None:
    try:
        with open(SQL_INIT_PATH, "r", encoding="utf-8") as f:
            sql_script = f.read()

        conn = get_connection()
        with conn:
            conn.executescript(sql_script)
        conn.close()
        logger.info("Database initialized successfully.")
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        raise


def create_employee(name: str, department: str, salary: float, hire_date: str) -> int:
    try:
        conn = get_connection()
        with conn:
            cursor = conn.execute(
                """
                INSERT INTO employees (name, department, salary, hire_date)
                VALUES (?, ?, ?, ?)
                """,
                (name, department, salary, hire_date),
            )
            new_id = cursor.lastrowid
        conn.close()
        logger.info(f"Created new employee: id={new_id}, name={name}")
        return new_id
    except Exception as e:
        logger.error(f"Failed to create employee: {e}")
        raise


def get_all_employees() -> list:
    try:
        conn = get_connection()
        rows = conn.execute("SELECT * FROM employees ORDER BY employee_id").fetchall()
        conn.close()
        return [dict(row) for row in rows]
    except Exception as e:
        logger.error(f"Failed to fetch employees: {e}")
        raise


def get_employee_by_id(employee_id: int) -> Optional[dict]:
    try:
        conn = get_connection()
        row = conn.execute(
            "SELECT * FROM employees WHERE employee_id = ?", (employee_id,)
        ).fetchone()
        conn.close()
        return dict(row) if row else None
    except Exception as e:
        logger.error(f"Failed to fetch employee id={employee_id}: {e}")
        raise


def update_employee(
    employee_id: int, name: str, department: str, salary: float, hire_date: str
) -> bool:
    try:
        conn = get_connection()
        with conn:
            cursor = conn.execute(
                """
                UPDATE employees
                SET name = ?, department = ?, salary = ?, hire_date = ?
                WHERE employee_id = ?
                """,
                (name, department, salary, hire_date, employee_id),
            )
            updated = cursor.rowcount > 0
        conn.close()
        if updated:
            logger.info(f"Updated employee id={employee_id}")
        else:
            logger.warning(f"Attempted to update non-existent employee id={employee_id}")
        return updated
    except Exception as e:
        logger.error(f"Failed to update employee id={employee_id}: {e}")
        raise


def delete_employee(employee_id: int) -> bool:
    try:
        conn = get_connection()
        with conn:
            cursor = conn.execute(
                "DELETE FROM employees WHERE employee_id = ?", (employee_id,)
            )
            deleted = cursor.rowcount > 0
        conn.close()
        if deleted:
            logger.info(f"Deleted employee id={employee_id}")
        else:
            logger.warning(f"Attempted to delete non-existent employee id={employee_id}")
        return deleted
    except Exception as e:
        logger.error(f"Failed to delete employee id={employee_id}: {e}")
        raise
