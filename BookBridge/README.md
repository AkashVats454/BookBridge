# BookBridge - Library Management System

A full-stack library management application built with FastAPI, Next.js/React, and PostgreSQL.

## Features

- **Book Management**: Add, update, and manage library books inventory
- **Member Management**: Track library members and their information
- **Borrowing System**: Record book borrowing and return operations
- **Overdue Tracking**: Automatic detection of overdue books
- **Book Availability**: Real-time tracking of available book copies

## Architecture

```
BookBridge/
├── backend/              # FastAPI REST API
│   ├── app/
│   │   ├── models/      # SQLAlchemy ORM models
│   │   ├── routes/      # API endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   ├── db/          # Database configuration
│   │   └── main.py      # FastAPI application
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/             # Next.js React application
│   ├── src/
│   │   ├── pages/       # Next.js pages
│   │   ├── components/  # React components
│   │   └── services/    # API client
│   ├── package.json
│   └── Dockerfile
├── docker-compose.yml
└── README.md
```

## Database Schema

### Books Table
- `id`: Primary key
- `title`: Book title
- `author`: Author name
- `isbn`: International Standard Book Number (unique)
- `description`: Book description
- `total_copies`: Total copies in library
- `available_copies`: Available copies for borrowing
- `created_at`, `updated_at`: Timestamps

### Members Table
- `id`: Primary key
- `name`: Member name
- `email`: Email (unique)
- `phone`: Phone number
- `address`: Member address
- `membership_date`: Date member joined
- `created_at`, `updated_at`: Timestamps

### Borrowings Table
- `id`: Primary key
- `book_id`: Foreign key to Books
- `member_id`: Foreign key to Members
- `borrowed_date`: Date book was borrowed
- `due_date`: Expected return date (14 days default)
- `returned_date`: Actual return date
- `is_returned`: Boolean flag for return status
- `created_at`, `updated_at`: Timestamps

## Prerequisites

- Docker & Docker Compose (recommended)
- OR
  - Python 3.11+
  - Node.js 18+
  - PostgreSQL 15+

## Quick Start with Docker

1. **Clone/Navigate to the project**:
   ```bash
   cd BookBridge
   ```

2. **Start all services**:
   ```bash
   docker-compose up --build
   ```

3. **Access the application**:
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## Manual Setup

### Backend Setup

1. **Navigate to backend directory**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up PostgreSQL**:
   ```bash
   # Create database
   createdb bookbridge_db
   
   # Or use Docker for PostgreSQL:
   docker run --name bookbridge_postgres \
     -e POSTGRES_USER=bookbridge_user \
     -e POSTGRES_PASSWORD=bookbridge_password \
     -e POSTGRES_DB=bookbridge_db \
     -p 5432:5432 \
     -d postgres:15-alpine
   ```

5. **Update `.env` file** (if needed):
   ```
   DATABASE_URL=postgresql://bookbridge_user:bookbridge_password@localhost:5432/bookbridge_db
   HOST=0.0.0.0
   PORT=8000
   DEBUG=True
   ```

6. **Run the server**:
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend Setup

1. **Navigate to frontend directory**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Set up environment**:
   ```bash
   # .env.local
   NEXT_PUBLIC_API_URL=http://localhost:8000
   ```

4. **Start development server**:
   ```bash
   npm run dev
   ```

5. **Access the app**:
   - Open http://localhost:3000 in your browser

## API Endpoints

### Books
- `POST /books` - Create a new book
- `GET /books` - List all books (paginated)
- `GET /books/{book_id}` - Get book details
- `PUT /books/{book_id}` - Update book
- `DELETE /books/{book_id}` - Delete book

### Members
- `POST /members` - Create a new member
- `GET /members` - List all members (paginated)
- `GET /members/{member_id}` - Get member details
- `PUT /members/{member_id}` - Update member
- `DELETE /members/{member_id}` - Delete member

### Borrowings
- `POST /borrowings` - Record a book borrowing
- `GET /borrowings` - List all borrowings (paginated)
- `GET /borrowings/{borrowing_id}` - Get borrowing details
- `GET /borrowings/member/{member_id}` - Get borrowings for a member
- `POST /borrowings/{borrowing_id}/return` - Return a borrowed book
- `GET /borrowings/overdue/list` - Get all overdue borrowings

## Example API Usage

### Create a Book
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

### Create a Member
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

### Record a Borrowing
```bash
curl -X POST http://localhost:8000/borrowings \
  -H "Content-Type: application/json" \
  -d '{
    "book_id": 1,
    "member_id": 1
  }'
```

### Return a Book
```bash
curl -X POST http://localhost:8000/borrowings/1/return \
  -H "Content-Type: application/json"
```

## Features Implemented

✅ Book CRUD operations
✅ Member CRUD operations
✅ Borrowing recording
✅ Book return tracking
✅ Overdue book detection
✅ Book availability management
✅ Modern React UI with Tailwind CSS
✅ RESTful API with proper error handling
✅ Database relationships and validation
✅ Docker containerization
✅ API documentation (Swagger)

## Error Handling

The API includes proper error handling for:
- Duplicate ISBN/Email
- Out of stock books
- Member trying to borrow same book twice
- Invalid book/member IDs
- Returning already returned books
- Input validation

## Testing

To test the application:

1. **Access Swagger UI**: http://localhost:8000/docs
2. **Use the interactive API documentation to test endpoints**
3. **Or use the frontend UI**: http://localhost:3000

## Environment Variables

### Backend (.env)
```
DATABASE_URL=postgresql://user:password@host:port/database
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=http://localhost:8000
```

## Project Structure Explanation

### Backend
- **models/**: SQLAlchemy ORM models for database entities
- **routes/**: FastAPI route handlers for endpoints
- **schemas/**: Pydantic models for request/response validation
- **db/**: Database connection and session management
- **main.py**: FastAPI application initialization and configuration

### Frontend
- **pages/**: Next.js pages (Home, Books, Members, Borrowings)
- **services/**: Axios API client for backend communication
- **styles/**: Global CSS and Tailwind configuration

## Future Enhancements

- User authentication and authorization
- Fine calculation for overdue books
- Book search and filtering
- Member activity history
- Email notifications for due dates
- Book recommendations
- Admin dashboard with statistics
- Export/Import functionality

## Troubleshooting

### Database Connection Issues
- Ensure PostgreSQL is running
- Check DATABASE_URL in `.env`
- Verify credentials and port

### API Not Responding
- Check if FastAPI server is running on port 8000
- Verify NEXT_PUBLIC_API_URL in frontend `.env.local`
- Check network connectivity

### Frontend Not Loading
- Ensure Node.js dependencies are installed
- Check if frontend server is running on port 3000
- Clear browser cache if necessary

## License

This project is provided as-is for educational purposes.

## Support

For issues or questions, please check:
1. API Documentation: http://localhost:8000/docs
2. Project structure and README
3. Error messages in browser console and terminal
