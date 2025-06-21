# FastAPI Task Manager

This project is a lightweight and secure task management backend built with **FastAPI** and **PostgreSQL**. It enables users to register, authenticate using JWT, and perform all standard task operations (CRUD). The API is designed to be clean, asynchronous, and easy to extend.

---

## Features

- **User Registration & Authentication**  
  Secure login with hashed passwords and JWT tokens.

- **Task Management**  
  Create, view, update, delete, and filter tasks.

- **Role Isolation**  
  Each user can only see and modify their own tasks.

- **Status Filtering**  
  Tasks can be filtered by status: `New`, `In Progress`, or `Completed`.

- **Modern Stack**  
  - FastAPI  
  - PostgreSQL  
  - SQLAlchemy Core  
  - Asyncpg  
  - Passlib (bcrypt)  
  - Pydantic

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fastapi-task-manager.git
cd fastapi-task-manager
