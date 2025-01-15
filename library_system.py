import sqlite3
from datetime import datetime, timedelta

class LibrarySystem:
    def __init__(self, db_name="library.db"):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()
        self.setup_database()
    
    def setup_database(self):
        """Create necessary tables if they don't exist"""
        self.cursor.executescript('''
            CREATE TABLE IF NOT EXISTS books (
                book_id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                isbn TEXT UNIQUE,
                status TEXT DEFAULT 'available'
            );

            CREATE TABLE IF NOT EXISTS members (
                member_id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                email TEXT UNIQUE,
                join_date DATE
            );

            CREATE TABLE IF NOT EXISTS loans (
                loan_id INTEGER PRIMARY KEY,
                book_id INTEGER,
                member_id INTEGER,
                loan_date DATE,
                due_date DATE,
                return_date DATE,
                FOREIGN KEY (book_id) REFERENCES books (book_id),
                FOREIGN KEY (member_id) REFERENCES members (member_id)
            );
        ''')
        self.conn.commit()

    def add_book(self, title, author, isbn):
        """Add a new book to the library"""
        try:
            self.cursor.execute('''
                INSERT INTO books (title, author, isbn)
                VALUES (?, ?, ?)
            ''', (title, author, isbn))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def add_member(self, name, email):
        """Register a new library member"""
        try:
            self.cursor.execute('''
                INSERT INTO members (name, email, join_date)
                VALUES (?, ?, ?)
            ''', (name, email, datetime.now().date()))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            return False

    def loan_book(self, book_id, member_id):
        """Loan a book to a member"""
        # Check if book is available
        self.cursor.execute('SELECT status FROM books WHERE book_id = ?', (book_id,))
        result = self.cursor.fetchone()
        
        if result and result[0] == 'available':
            loan_date = datetime.now().date()
            due_date = loan_date + timedelta(days=14)  # 2-week loan period
            
            self.cursor.execute('''
                INSERT INTO loans (book_id, member_id, loan_date, due_date)
                VALUES (?, ?, ?, ?)
            ''', (book_id, member_id, loan_date, due_date))
            
            # Update book status
            self.cursor.execute('''
                UPDATE books SET status = 'loaned'
                WHERE book_id = ?
            ''', (book_id,))
            
            self.conn.commit()
            return True
        return False

    def return_book(self, book_id):
        """Process a book return"""
        self.cursor.execute('''
            UPDATE loans 
            SET return_date = ?
            WHERE book_id = ? AND return_date IS NULL
        ''', (datetime.now().date(), book_id))
        
        self.cursor.execute('''
            UPDATE books 
            SET status = 'available'
            WHERE book_id = ?
        ''', (book_id,))
        
        self.conn.commit()

    def search_books(self, query):
        """Search for books by title or author"""
        self.cursor.execute('''
            SELECT * FROM books
            WHERE title LIKE ? OR author LIKE ?
        ''', (f'%{query}%', f'%{query}%'))
        return self.cursor.fetchall()

    def get_overdue_books(self):
        """Get all overdue books"""
        self.cursor.execute('''
            SELECT b.title, m.name, l.due_date
            FROM loans l
            JOIN books b ON l.book_id = b.book_id
            JOIN members m ON l.member_id = m.member_id
            WHERE l.return_date IS NULL
            AND l.due_date < ?
        ''', (datetime.now().date(),))
        return self.cursor.fetchall()

    def close(self):
        """Close the database connection"""
        self.conn.close()