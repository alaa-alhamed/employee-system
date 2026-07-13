# Employee System — FastAPI + Streamlit

An employee data management system[cite: 1]. It consists of:
- **Backend**: FastAPI + SQLite (provides REST API only)[cite: 1].
- **Frontend**: Streamlit (dashboard + analytics + employee management forms)[cite: 1].

## Project Structure
employee_system/
├── config.py                  # All settings (paths, URLs, etc.)
├── requirements.txt
├── docker-compose.yml
├── database/
│   └── script.sql             # Table creation script
├── utils/
│   ├── logger.py               # Logger setup
│   └── database.py             # SQLite connection + CRUD functions
├── backend/
│   ├── main.py                 # FastAPI application and endpoints
│   └── Dockerfile
└── frontend/
├── app.py                  # Main welcome page
├── api_client.py           # Communication with the backend via requests
├── pages/
│   ├── 1_Dashboard.py
│   └── 2_Employee_Management.py
└── Dockerfile
