from library_system import LibrarySystem

# Start up our library system
library = LibrarySystem()

# Add a book
library.add_book("Harry Potter", "J.K. Rowling", "12345")

# Add a member
library.add_member("Bob", "bob@email.com")

# Let Bob borrow Harry Potter
library.loan_book(1, 1)

# When Bob returns the book
library.return_book(1)