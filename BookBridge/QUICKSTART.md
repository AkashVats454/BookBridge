# BookBridge - Quick Start Guide

## 🚀 Start the Project (Recommended: Using Docker)

### Prerequisites
- Docker & Docker Compose installed
- OR manually: Python 3.11+, Node.js 18+, PostgreSQL 15+

### Option 1: Docker (Easiest)

1. **Navigate to project root:**
   ```bash
   cd BookBridge
   ```

2. **Start all services:**
   ```bash
   docker-compose up --build
   ```

3. **Wait for services to start** (2-3 minutes first time):
   - PostgreSQL database will initialize
   - FastAPI backend will start
   - React frontend will build and start

4. **Access the application:**
   - 🌐 Frontend: http://localhost:3000
   - 🔌 API: http://localhost:8000
   - 📚 API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup:
```bash
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Linux/Mac:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start PostgreSQL (if not already running)
# Option A: Using Docker
docker run --name bookbridge_postgres \
  -e POSTGRES_USER=bookbridge_user \
  -e POSTGRES_PASSWORD=bookbridge_password \
  -e POSTGRES_DB=bookbridge_db \
  -p 5432:5432 \
  -d postgres:15-alpine

# Option B: Using local PostgreSQL
createdb bookbridge_db

# Run the server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

#### Frontend Setup (in another terminal):
```bash
# Navigate to frontend
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev
```

Access at http://localhost:3000

## 🧪 Test the API

### Using the Test Script:
```bash
python test_api.py
```

This will:
- Create sample books
- Create sample members
- Record borrowings
- Demonstrate all API operations

### Using Swagger UI:
1. Visit http://localhost:8000/docs
2. Try out endpoints directly in the UI

### Using cURL:

**Create a Book:**
```bash
curl -X POST http://localhost:8000/books \
  -H "Content-Type: application/json" \
  -d '{
    "title": "The Great Gatsby",
    "author": "F. Scott Fitzgerald",
    "isbn": "978-0743273565",
    "description": "A classic American novel",
    "total_copies": 3
  }'
```

**Create a Member:**
```bash
curl -X POST http://localhost:8000/members \
  -H "Content-Type: application/json" \
  -d '{
    "name": "John Doe",
    "email": "john@example.com",
    "phone": "555-1234",
    "address": "123 Main St"
  }'
```

**Record a Borrowing:**
```bash
curl -X POST http://localhost:8000/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1
  }'
```

**Return a Book:**
```bash
curl -X POST http://localhost:8000/borrowings/1/return
```

## 📁 Project Structure

```
BookBridge/
├── backend/
│   ├── app/
│   │   ├── models/          # Database models
│   │   ├── routes/          # API endpoints
│   │   ├── schemas/         # Request/response schemas
│   │   ├── db/              # Database config
│   │   └── main.py          # FastAPI app
│   ├── requirements.txt
│   ├── Dockerfile
│   └── .env
│
├── frontend/
│   ├── src/
│   │   ├── pages/           # React pages
│   │   ├── components/      # React components
│   │   ├── services/        # API client
│   │   └── styles/          # CSS styles
│   ├── package.json
│   ├── Dockerfile
│   └── .env.local
│
├── docker-compose.yml       # Docker configuration
├── README.md                # Full documentation
├── test_api.py              # Test script
├── setup.sh / setup.bat     # Setup scripts
└── .gitignore
```

## 🎯 Key Features

✅ Book management (add/edit/delete)
✅ Member management
✅ Borrowing/return operations
✅ Overdue tracking
✅ Book availability management
✅ Modern React UI
✅ RESTful API with Swagger docs
✅ PostgreSQL database
✅ Docker support
✅ Error handling & validation

## 🔧 Environment Variables

**Backend** (`backend/.env`):
```
DATABASE_URL=postgresql://bookbridge_user:bookbridge_password@localhost:5432/bookbridge_db
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

**Frontend** (`frontend/.env.local`):
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## 📊 Database

Automatically created with the following tables:
- **books**: Book inventory
- **members**: Library members
- **borrowings**: Borrowing records

## 🛠️ Troubleshooting

**API not connecting:**
- Check if backend is running: `http://localhost:8000/health`
- Verify DATABASE_URL in `.env`

**Database connection failed:**
- Ensure PostgreSQL is running
- Check credentials in `.env`

**Frontend not loading:**
- Check if NEXT_PUBLIC_API_URL is correct
- Clear browser cache

**Port already in use:**
- Change port in `.env` or docker-compose.yml
- Or stop the service using that port

## 📖 Documentation

- Full docs: See [README.md](README.md)
- API docs: http://localhost:8000/docs
- Database schema: See [README.md](README.md#database-schema)

## 💻 Using the Web UI

1. Go to http://localhost:3000
2. Navigate using the menu:
   - **Books**: Add/view/delete books
   - **Members**: Add/view/delete members
   - **Borrowings**: Record and track borrowings

## 🚀 Deployment

For production:
1. Set `DEBUG=False` in backend `.env`
2. Use environment-specific configurations
3. Set appropriate database credentials
4. Use a production ASGI server (Gunicorn, etc.)
5. Configure CORS appropriately
6. Use HTTPS

## 📝 Notes

- Default borrow period: 14 days
- Duplicate ISBNs and emails are prevented
- Members can't borrow the same book twice
- Book availability is automatically updated
- All timestamps are in UTC

## Need Help?

- Check API documentation: http://localhost:8000/docs
- Review [README.md](README.md) for detailed information
- Check terminal logs for error messages
- Test with `test_api.py` script
