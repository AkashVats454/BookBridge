"""
Sample API client to demonstrate BookBridge API usage
"""
import requests
import json
from datetime import datetime

BASE_URL = 'http://localhost:5000/api'

class BookBridgeClient:
    def __init__(self, base_url=BASE_URL):
        self.base_url = base_url
        self.session = requests.Session()
    
    # ==================== MEMBERS ====================
    def create_member(self, name, email, phone=None, address=None):
        """Create a new member"""
        payload = {
            'name': name,
            'email': email,
            'phone': phone,
            'address': address
        }
        response = self.session.post(f'{self.base_url}/members', json=payload)
        return response.json()
    
    def get_member(self, member_id):
        """Get member details"""
        response = self.session.get(f'{self.base_url}/members/{member_id}')
        return response.json()
    
    def list_members(self, page=1, per_page=10):
        """List all members"""
        response = self.session.get(f'{self.base_url}/members?page={page}&per_page={per_page}')
        return response.json()
    
    def update_member(self, member_id, **kwargs):
        """Update member details"""
        response = self.session.put(f'{self.base_url}/members/{member_id}', json=kwargs)
        return response.json()
    
    # ==================== BOOKS ====================
    def create_book(self, title, author, isbn=None, category=None, 
                    publisher=None, publication_year=None, total_copies=1, description=None):
        """Create a new book"""
        payload = {
            'title': title,
            'author': author,
            'isbn': isbn,
            'category': category,
            'publisher': publisher,
            'publication_year': publication_year,
            'total_copies': total_copies,
            'description': description
        }
        response = self.session.post(f'{self.base_url}/books', json=payload)
        return response.json()
    
    def get_book(self, book_id):
        """Get book details"""
        response = self.session.get(f'{self.base_url}/books/{book_id}')
        return response.json()
    
    def list_books(self, page=1, per_page=10, category=None):
        """List all books"""
        params = f'page={page}&per_page={per_page}'
        if category:
            params += f'&category={category}'
        response = self.session.get(f'{self.base_url}/books?{params}')
        return response.json()
    
    def update_book(self, book_id, **kwargs):
        """Update book details"""
        response = self.session.put(f'{self.base_url}/books/{book_id}', json=kwargs)
        return response.json()
    
    # ==================== BORROWING ====================
    def borrow_book(self, member_id, book_id):
        """Record a book borrow"""
        payload = {
            'member_id': member_id,
            'book_id': book_id
        }
        response = self.session.post(f'{self.base_url}/borrowing/borrow', json=payload)
        return response.json()
    
    def return_book(self, borrowing_id):
        """Record a book return"""
        response = self.session.put(f'{self.base_url}/borrowing/return/{borrowing_id}')
        return response.json()
    
    def get_member_borrowed_books(self, member_id, status='borrowed'):
        """Get books borrowed by a member"""
        response = self.session.get(f'{self.base_url}/borrowing/member/{member_id}?status={status}')
        return response.json()
    
    def list_borrowing_records(self, page=1, per_page=10, status=None):
        """List all borrowing records"""
        params = f'page={page}&per_page={per_page}'
        if status:
            params += f'&status={status}'
        response = self.session.get(f'{self.base_url}/borrowing?{params}')
        return response.json()
    
    def get_overdue_books(self):
        """Get all overdue books"""
        response = self.session.get(f'{self.base_url}/borrowing/overdue')
        return response.json()


def demo():
    """Run a demo of the API"""
    client = BookBridgeClient()
    
    print("=" * 60)
    print("BookBridge API Demo")
    print("=" * 60)
    
    # Create members
    print("\n1. Creating members...")
    member1 = client.create_member(
        name="Alice Johnson",
        email="alice@example.com",
        phone="555-1001",
        address="123 Main St"
    )
    print(f"✓ Created member: {member1['data']['name']}")
    member1_id = member1['data']['id']
    
    member2 = client.create_member(
        name="Bob Smith",
        email="bob@example.com",
        phone="555-1002",
        address="456 Oak Ave"
    )
    print(f"✓ Created member: {member2['data']['name']}")
    member2_id = member2['data']['id']
    
    # Create books
    print("\n2. Creating books...")
    book1 = client.create_book(
        title="The Great Gatsby",
        author="F. Scott Fitzgerald",
        isbn="978-0743273565",
        category="Fiction",
        publisher="Scribner",
        publication_year=1925,
        total_copies=3,
        description="A classic novel of the Jazz Age"
    )
    print(f"✓ Created book: {book1['data']['title']}")
    book1_id = book1['data']['id']
    
    book2 = client.create_book(
        title="To Kill a Mockingbird",
        author="Harper Lee",
        isbn="978-0061120084",
        category="Fiction",
        publisher="J.B. Lippincott",
        publication_year=1960,
        total_copies=2,
        description="An American classic about race and justice"
    )
    print(f"✓ Created book: {book2['data']['title']}")
    book2_id = book2['data']['id']
    
    # Borrow books
    print("\n3. Recording book borrows...")
    borrow1 = client.borrow_book(member1_id, book1_id)
    if borrow1['success']:
        print(f"✓ {member1['data']['name']} borrowed '{book1['data']['title']}'")
        borrowing_id_1 = borrow1['data']['id']
    
    borrow2 = client.borrow_book(member2_id, book2_id)
    if borrow2['success']:
        print(f"✓ {member2['data']['name']} borrowed '{book2['data']['title']}'")
        borrowing_id_2 = borrow2['data']['id']
    
    # Query borrowed books
    print("\n4. Querying borrowed books...")
    member1_books = client.get_member_borrowed_books(member1_id, status='borrowed')
    print(f"✓ Books borrowed by {member1['data']['name']}:")
    for record in member1_books['data']:
        print(f"  - {record['book_title']} (Due: {record['due_date'][:10]})")
    
    # Check availability
    print("\n5. Checking book availability...")
    book1_info = client.get_book(book1_id)
    print(f"✓ {book1_info['data']['title']}: {book1_info['data']['available_copies']}/{book1_info['data']['total_copies']} copies available")
    
    # Return a book
    print("\n6. Recording book returns...")
    return_result = client.return_book(borrowing_id_1)
    if return_result['success']:
        print(f"✓ Book returned: {book1['data']['title']}")
    
    # List all members
    print("\n7. Listing all members...")
    members = client.list_members(per_page=5)
    print(f"✓ Total members: {members['pagination']['total']}")
    
    # List all books
    print("\n8. Listing all books...")
    books = client.list_books(per_page=5)
    print(f"✓ Total books: {books['pagination']['total']}")
    
    print("\n" + "=" * 60)
    print("Demo completed!")
    print("=" * 60)


if __name__ == '__main__':
    # Make sure the API is running before running this demo
    try:
        demo()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to API at http://localhost:5000")
        print("Make sure the Flask server is running: python app.py")
    except Exception as e:
        print(f"Error: {e}")
