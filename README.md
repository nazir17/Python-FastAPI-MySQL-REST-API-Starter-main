# Python FastAPI MySQL REST API

This is a sample REST API that demonstrates how to use FastAPI with MySQL.
## Features

## Features

*   **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
*   **MySQL**: A popular open-source relational database.
*   **SQLAlchemy**: A SQL toolkit and Object-Relational Mapper (ORM) for Python.
*   **Pydantic**: Data validation and settings management using Python type annotations.
*   **JWT Authentication**: Secure your endpoints with JSON Web Tokens.
*   **Role-Based Access Control (RBAC)**: Restrict access to certain endpoints based on user roles.
*   **Custom Exception Handling**: A robust system for handling and formatting exceptions.
*   **Async Support**: Asynchronous views for I/O-bound tasks.
*   **Authentication APIs**
*   **User CRUD APIs**
*   **Swagger documentation**

### Prerequisites

*   Python 3.7+
*   MySQL Server

## Tech Stack

- Python
- FastAPI
- MySQL
- Pydantic

## Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/iamtalibaziz/Python-FastAPI-MySQL-REST-API-Starter.git
   cd Python-FastAPI-MySQL-REST-API-Starter
   ```

2. **Create a virtual environment and activate it:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```

3. **Install the dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up the database:**
    *   Create a MySQL database.
    *   Copy the `.env.example` file to `.env` and update the database connection details:

        ```env
        ENVIRONMENT=development
        PORT=8000
        DB_HOST=localhost
        DB_USER=your_db_user
        DB_PASSWORD=your_db_password
        DB_NAME=your_db_name
        JWT_SECRET=your_jwt_secret
        ```

5. **Run the application:**
   ```bash
    python run.py
    ```

## API Documentation

Once the application is running, you can access the Swagger UI for API documentation at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).
