from flask import Blueprint, request, jsonify
from datetime import datetime, timedelta
from models import db, Member, Book, BorrowingRecord
from sqlalchemy.exc import IntegrityError

# Create blueprints
members_bp = Blueprint('members', __name__, url_prefix='/api/members')
books_bp = Blueprint('books', __name__, url_prefix='/api/books')
borrowing_bp = Blueprint('borrowing', __name__, url_prefix='/api/borrowing')

# ======================== MEMBERS ENDPOINTS ========================

@members_bp.route('', methods=['GET'])
def get_members():
    """Get all members"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        query = Member.query
        total = query.count()
        members = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [m.to_dict() for m in members.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['GET'])
def get_member(member_id):
    """Get a specific member"""
    try:
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        return jsonify({'success': True, 'data': member.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@members_bp.route('', methods=['POST'])
def create_member():
    """Create a new member"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('name') or not data.get('email'):
            return jsonify({'success': False, 'error': 'Missing required fields: name, email'}), 400
        
        # Check if email already exists
        if Member.query.filter_by(email=data['email']).first():
            return jsonify({'success': False, 'error': 'Email already exists'}), 400
        
        member = Member(
            name=data['name'],
            email=data['email'],
            phone=data.get('phone'),
            address=data.get('address'),
            is_active=data.get('is_active', True)
        )
        
        db.session.add(member)
        db.session.commit()
        
        return jsonify({'success': True, 'data': member.to_dict(), 'message': 'Member created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'Email already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['PUT'])
def update_member(member_id):
    """Update a member"""
    try:
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'name' in data:
            member.name = data['name']
        if 'email' in data:
            # Check if new email is not already taken
            existing = Member.query.filter_by(email=data['email']).first()
            if existing and existing.id != member_id:
                return jsonify({'success': False, 'error': 'Email already exists'}), 400
            member.email = data['email']
        if 'phone' in data:
            member.phone = data['phone']
        if 'address' in data:
            member.address = data['address']
        if 'is_active' in data:
            member.is_active = data['is_active']
        
        member.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'data': member.to_dict(), 'message': 'Member updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@members_bp.route('/<int:member_id>', methods=['DELETE'])
def delete_member(member_id):
    """Delete a member"""
    try:
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        
        db.session.delete(member)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Member deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== BOOKS ENDPOINTS ========================

@books_bp.route('', methods=['GET'])
def get_books():
    """Get all books"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        category = request.args.get('category')
        
        query = Book.query
        if category:
            query = query.filter_by(category=category)
        
        total = query.count()
        books = query.paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [b.to_dict() for b in books.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get a specific book"""
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'error': 'Book not found'}), 404
        return jsonify({'success': True, 'data': book.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@books_bp.route('', methods=['POST'])
def create_book():
    """Create a new book"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or not data.get('title') or not data.get('author'):
            return jsonify({'success': False, 'error': 'Missing required fields: title, author'}), 400
        
        book = Book(
            title=data['title'],
            author=data['author'],
            isbn=data.get('isbn'),
            category=data.get('category'),
            publisher=data.get('publisher'),
            publication_year=data.get('publication_year'),
            total_copies=data.get('total_copies', 1),
            available_copies=data.get('total_copies', 1),
            description=data.get('description')
        )
        
        db.session.add(book)
        db.session.commit()
        
        return jsonify({'success': True, 'data': book.to_dict(), 'message': 'Book created successfully'}), 201
    except IntegrityError as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': 'ISBN already exists'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update a book"""
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'error': 'Book not found'}), 404
        
        data = request.get_json()
        
        # Update fields
        if 'title' in data:
            book.title = data['title']
        if 'author' in data:
            book.author = data['author']
        if 'isbn' in data:
            existing = Book.query.filter_by(isbn=data['isbn']).first()
            if existing and existing.id != book_id:
                return jsonify({'success': False, 'error': 'ISBN already exists'}), 400
            book.isbn = data['isbn']
        if 'category' in data:
            book.category = data['category']
        if 'publisher' in data:
            book.publisher = data['publisher']
        if 'publication_year' in data:
            book.publication_year = data['publication_year']
        if 'total_copies' in data:
            book.total_copies = data['total_copies']
        if 'available_copies' in data:
            book.available_copies = data['available_copies']
        if 'description' in data:
            book.description = data['description']
        
        book.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({'success': True, 'data': book.to_dict(), 'message': 'Book updated successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@books_bp.route('/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete a book"""
    try:
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'error': 'Book not found'}), 404
        
        db.session.delete(book)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Book deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

# ======================== BORROWING ENDPOINTS ========================

@borrowing_bp.route('/borrow', methods=['POST'])
def borrow_book():
    """Record a book borrow"""
    try:
        data = request.get_json()
        
        # Validation
        if not data or 'member_id' not in data or 'book_id' not in data:
            return jsonify({'success': False, 'error': 'Missing required fields: member_id, book_id'}), 400
        
        member_id = data['member_id']
        book_id = data['book_id']
        
        # Check if member exists and is active
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        if not member.is_active:
            return jsonify({'success': False, 'error': 'Member is not active'}), 400
        
        # Check if book exists
        book = Book.query.get(book_id)
        if not book:
            return jsonify({'success': False, 'error': 'Book not found'}), 404
        
        # Check if book is available
        if book.available_copies <= 0:
            return jsonify({'success': False, 'error': 'Book is not available. All copies are checked out'}), 400
        
        # Check if member already has this book checked out
        existing_borrow = BorrowingRecord.query.filter_by(
            member_id=member_id,
            book_id=book_id,
            status='borrowed'
        ).first()
        if existing_borrow:
            return jsonify({'success': False, 'error': 'Member already has this book checked out'}), 400
        
        # Create borrowing record
        borrow_date = datetime.utcnow()
        due_date = borrow_date + timedelta(days=14)  # 14-day loan period
        
        borrowing_record = BorrowingRecord(
            member_id=member_id,
            book_id=book_id,
            borrow_date=borrow_date,
            due_date=due_date,
            status='borrowed'
        )
        
        # Decrease available copies
        book.available_copies -= 1
        book.updated_at = datetime.utcnow()
        
        db.session.add(borrowing_record)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': borrowing_record.to_dict(),
            'message': 'Book borrowed successfully'
        }), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@borrowing_bp.route('/return/<int:borrowing_id>', methods=['PUT'])
def return_book(borrowing_id):
    """Record a book return"""
    try:
        borrowing_record = BorrowingRecord.query.get(borrowing_id)
        if not borrowing_record:
            return jsonify({'success': False, 'error': 'Borrowing record not found'}), 404
        
        if borrowing_record.status != 'borrowed':
            return jsonify({'success': False, 'error': 'Book is not currently borrowed'}), 400
        
        return_date = datetime.utcnow()
        borrowing_record.return_date = return_date
        borrowing_record.status = 'returned'
        
        # Calculate fine if overdue
        if return_date > borrowing_record.due_date:
            days_overdue = (return_date - borrowing_record.due_date).days
            borrowing_record.fine_amount = days_overdue * 0.50  # $0.50 per day
        
        # Increase available copies
        book = Book.query.get(borrowing_record.book_id)
        if book:
            book.available_copies += 1
            book.updated_at = datetime.utcnow()
        
        borrowing_record.updated_at = datetime.utcnow()
        db.session.commit()
        
        return jsonify({
            'success': True,
            'data': borrowing_record.to_dict(),
            'message': 'Book returned successfully'
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500

@borrowing_bp.route('/member/<int:member_id>', methods=['GET'])
def get_member_borrowed_books(member_id):
    """Get all books borrowed by a member"""
    try:
        member = Member.query.get(member_id)
        if not member:
            return jsonify({'success': False, 'error': 'Member not found'}), 404
        
        status_filter = request.args.get('status', 'borrowed')  # 'borrowed', 'returned', or 'all'
        
        query = BorrowingRecord.query.filter_by(member_id=member_id)
        if status_filter != 'all':
            query = query.filter_by(status=status_filter)
        
        records = query.order_by(BorrowingRecord.borrow_date.desc()).all()
        
        return jsonify({
            'success': True,
            'member_id': member_id,
            'member_name': member.name,
            'status_filter': status_filter,
            'data': [r.to_dict() for r in records]
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@borrowing_bp.route('', methods=['GET'])
def get_all_borrowing_records():
    """Get all borrowing records with optional filters"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        status_filter = request.args.get('status')
        
        query = BorrowingRecord.query
        if status_filter:
            query = query.filter_by(status=status_filter)
        
        total = query.count()
        records = query.order_by(BorrowingRecord.borrow_date.desc()).paginate(page=page, per_page=per_page)
        
        return jsonify({
            'success': True,
            'data': [r.to_dict() for r in records.items],
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': total,
                'pages': (total + per_page - 1) // per_page
            }
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@borrowing_bp.route('/overdue', methods=['GET'])
def get_overdue_books():
    """Get all overdue books"""
    try:
        now = datetime.utcnow()
        overdue_records = BorrowingRecord.query.filter(
            BorrowingRecord.due_date < now,
            BorrowingRecord.status == 'borrowed'
        ).order_by(BorrowingRecord.due_date).all()
        
        data = []
        for record in overdue_records:
            record_data = record.to_dict()
            record_data['days_overdue'] = (now - record.due_date).days
            record_data['fine_amount'] = record.calculate_fine()
            data.append(record_data)
        
        return jsonify({
            'success': True,
            'data': data
        }), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@borrowing_bp.route('/<int:borrowing_id>', methods=['GET'])
def get_borrowing_record(borrowing_id):
    """Get a specific borrowing record"""
    try:
        record = BorrowingRecord.query.get(borrowing_id)
        if not record:
            return jsonify({'success': False, 'error': 'Borrowing record not found'}), 404
        return jsonify({'success': True, 'data': record.to_dict()}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
