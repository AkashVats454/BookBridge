#!/usr/bin/env python3
"""
Sample script to test BookBridge API
Run this script to populate the database with sample data and test endpoints
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def print_response(title, response):
    """Print API response in a readable format"""
    print(f"\n{'='*60}")
    print(f"{title}")
    print(f"{'='*60}")
    print(f"Status Code: {response.status_code}")
    try:
        print(json.dumps(response.json(), indent=2))
    except:
        print(response.text)

def test_health():
    """Test health endpoint"""
    response = requests.get(f"{BASE_URL}/health")
    print_response("Health Check", response)
    return response.status_code == 200

def test_create_books():
    """Create sample books"""
    books = [
        {
            "title": "The Great Gatsby",
            "author": "F. Scott Fitzgerald",
            "isbn": "978-0743273565",
            "description": "A classic American novel set in the Jazz Age",
            "total_copies": 3
        },
        {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "isbn": "978-0061120084",
            "description": "A gripping tale of racial injustice and childhood innocence",
            "total_copies": 2
        },
        {
            "title": "1984",
            "author": "George Orwell",
            "isbn": "978-0451524935",
            "description": "A dystopian social science fiction novel",
            "total_copies": 4
        },
        {
            "title": "Pride and Prejudice",
            "author": "Jane Austen",
            "isbn": "978-0141439518",
            "description": "A romantic novel of manners",
            "total_copies": 2
        }
    ]
    
    book_ids = []
    for book in books:
        response = requests.post(f"{BASE_URL}/books", json=book)
        print_response(f"Create Book: {book['title']}", response)
        if response.status_code == 201:
            book_ids.append(response.json()["id"])
    
    return book_ids

def test_list_books():
    """List all books"""
    response = requests.get(f"{BASE_URL}/books")
    print_response("List Books", response)
    return response.json()

def test_create_members():
    """Create sample members"""
    members = [
        {
            "name": "Alice Johnson",
            "email": "alice@example.com",
            "phone": "555-0101",
            "address": "123 Main St, Springfield"
        },
        {
            "name": "Bob Smith",
            "email": "bob@example.com",
            "phone": "555-0102",
            "address": "456 Oak Ave, Springfield"
        },
        {
            "name": "Carol Davis",
            "email": "carol@example.com",
            "phone": "555-0103",
            "address": "789 Pine Rd, Springfield"
        }
    ]
    
    member_ids = []
    for member in members:
        response = requests.post(f"{BASE_URL}/members", json=member)
        print_response(f"Create Member: {member['name']}", response)
        if response.status_code == 201:
            member_ids.append(response.json()["id"])
    
    return member_ids

def test_list_members():
    """List all members"""
    response = requests.get(f"{BASE_URL}/members")
    print_response("List Members", response)
    return response.json()

def test_create_borrowings(book_ids, member_ids):
    """Create borrowing records"""
    borrowings = [
        {"book_id": book_ids[0], "member_id": member_ids[0]},
        {"book_id": book_ids[1], "member_id": member_ids[0]},
        {"book_id": book_ids[2], "member_id": member_ids[1]},
        {"book_id": book_ids[3], "member_id": member_ids[2]}
    ]
    
    borrowing_ids = []
    for idx, borrowing in enumerate(borrowings):
        response = requests.post(f"{BASE_URL}/borrowings", json=borrowing)
        print_response(f"Record Borrowing {idx+1}", response)
        if response.status_code == 201:
            borrowing_ids.append(response.json()["id"])
    
    return borrowing_ids

def test_list_borrowings():
    """List all borrowings"""
    response = requests.get(f"{BASE_URL}/borrowings")
    print_response("List Borrowings", response)
    return response.json()

def test_member_borrowings(member_id):
    """Get borrowings for a specific member"""
    response = requests.get(f"{BASE_URL}/borrowings/member/{member_id}")
    print_response(f"Member {member_id} Borrowings", response)
    return response.json()

def test_return_book(borrowing_id):
    """Return a borrowed book"""
    response = requests.post(f"{BASE_URL}/borrowings/{borrowing_id}/return")
    print_response(f"Return Book - Borrowing {borrowing_id}", response)
    return response.status_code == 200

def test_overdue_borrowings():
    """Get overdue borrowings"""
    response = requests.get(f"{BASE_URL}/borrowings/overdue/list")
    print_response("Overdue Borrowings", response)
    return response.json()

def run_all_tests():
    """Run all test cases"""
    print("\n" + "="*60)
    print("BOOKBRIDGE API TEST SUITE")
    print("="*60)
    
    # Health check
    if not test_health():
        print("\n❌ API is not responding. Make sure the server is running.")
        return
    
    # Create books
    print("\n📚 Creating Books...")
    book_ids = test_create_books()
    
    # List books
    print("\n📚 Listing Books...")
    test_list_books()
    
    # Create members
    print("\n👥 Creating Members...")
    member_ids = test_create_members()
    
    # List members
    print("\n👥 Listing Members...")
    test_list_members()
    
    # Create borrowings
    print("\n📋 Recording Borrowings...")
    borrowing_ids = test_create_borrowings(book_ids, member_ids)
    
    # List borrowings
    print("\n📋 Listing Borrowings...")
    test_list_borrowings()
    
    # Get member borrowings
    if member_ids:
        print(f"\n📋 Getting Borrowings for Member {member_ids[0]}...")
        test_member_borrowings(member_ids[0])
    
    # Return a book
    if borrowing_ids:
        print(f"\n✅ Returning Book - Borrowing {borrowing_ids[0]}...")
        test_return_book(borrowing_ids[0])
    
    # Get overdue borrowings
    print("\n⏰ Checking Overdue Borrowings...")
    test_overdue_borrowings()
    
    print("\n" + "="*60)
    print("✅ TEST SUITE COMPLETED")
    print("="*60)
    print("\n💡 Tips:")
    print("- Check API documentation at: http://localhost:8000/docs")
    print("- Access the frontend at: http://localhost:3000")
    print("- Database contains test data that can be used for exploration")

if __name__ == "__main__":
    import sys
    try:
        run_all_tests()
    except requests.exceptions.ConnectionError:
        print("\n❌ Could not connect to the API")
        print("Make sure the FastAPI server is running at http://localhost:8000")
        print("\nTo start the server:")
        print("1. With Docker: docker-compose up")
        print("2. Without Docker: cd backend && uvicorn app.main:app --reload")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
