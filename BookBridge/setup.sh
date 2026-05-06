#!/bin/bash
# Quick setup script for BookBridge

echo "🚀 BookBridge - Quick Setup"
echo "=============================="

# Check if Docker is installed
if command -v docker &> /dev/null; then
    echo "✅ Docker found"
    echo ""
    echo "Starting services with Docker Compose..."
    docker-compose up --build
else
    echo "❌ Docker not found"
    echo ""
    echo "Manual Setup Instructions:"
    echo "=============================="
    echo ""
    echo "BACKEND SETUP:"
    echo "cd backend"
    echo "python -m venv venv"
    echo "source venv/bin/activate  # On Windows: venv\\Scripts\\activate"
    echo "pip install -r requirements.txt"
    echo "uvicorn app.main:app --reload"
    echo ""
    echo "FRONTEND SETUP (in another terminal):"
    echo "cd frontend"
    echo "npm install"
    echo "npm run dev"
    echo ""
    echo "DATABASE SETUP:"
    echo "createdb bookbridge_db"
    echo "Or use Docker: docker run --name bookbridge_postgres ..."
fi
