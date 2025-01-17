from library_system import LibrarySystem

# Start up our library system
library = LibrarySystem()

# Add some books
library.add_book("Harry Potter", "J.K. Rowling", "12345")
library.add_book("Lord of the Rings", "J.R.R. Tolkien", "67890")
library.add_book("The Great Gatsby", "F. Scott Fitzgerald", "11111")

# Add a member
library.add_member("Bob", "bob@email.com")

# Let Bob borrow Harry Potter
library.loan_book(1, 1)

# When Bob returns the book
library.return_book(1)
