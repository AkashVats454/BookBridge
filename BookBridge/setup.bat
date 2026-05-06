@echo off
REM Quick setup script for BookBridge on Windows

echo 🚀 BookBridge - Quick Setup
echo ==============================

REM Check if Docker is installed
where docker >nul 2>nul
if %ERRORLEVEL% EQU 0 (
    echo ✅ Docker found
    echo.
    echo Starting services with Docker Compose...
    docker-compose up --build
) else (
    echo ❌ Docker not found
    echo.
    echo Manual Setup Instructions:
    echo ==============================
    echo.
    echo BACKEND SETUP:
    echo cd backend
    echo python -m venv venv
    echo venv\Scripts\activate
    echo pip install -r requirements.txt
    echo uvicorn app.main:app --reload
    echo.
    echo FRONTEND SETUP (in another terminal^):
    echo cd frontend
    echo npm install
    echo npm run dev
    echo.
    echo DATABASE SETUP:
    echo createdb bookbridge_db
    echo Or use Docker: docker run --name bookbridge_postgres ...
)
