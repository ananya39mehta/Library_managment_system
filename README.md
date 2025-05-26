# Library Management System API

This is a Flask-based backend service for a Library Management System that allows for managing books, borrowers, loans, fines, and related entities.

## Features

- **Book Management**: Add, search, and list books with copies, languages, and categories.
- **Borrowing System**: Record borrowing and returning of book copies, with automatic due dates and fine calculation.
- **Fine Handling**: Calculate and record fines and payments.
- **Borrower Management**: Add, update, and view borrower information including loan history and fines.
- **Statistics Endpoint**: Fetch summary statistics like total books, active loans, and overdue books.

## Notable Design and Implementation Decisions
- **Clear separation between book metadata and physical copies**:Instead of treating each book as a unique item, we separate book metadata (like title, author, ISBN) from its physical copies. This allows us to manage multiple copies of the same book efficiently—each with its own availability and shelf location.

- **Smart handling of duplicate books**:
When a new book is added, the system checks if the ISBN already exists. If it does, we just add more copies instead of duplicating the book metadata. This keeps the database clean and avoids redundancy.

- **Fine-grained relationships using SQLAlchemy**:
We modeled relationships explicitly—like many-to-many between books and categories, and one-to-many between borrowers and loans. This makes it easy to query related data and scale the system as needed.

- **Automatic due date and fine calculation**:
When someone borrows a book, the due date is calculated based on their category (e.g., students vs faculty). If they return it late, the system automatically calculates a fine using a category-specific rate.

- **Consistent borrower experience**:
Borrower information includes their history, current loans, fines owed, and payment records—all in one place. This helps admins get a full picture at a glance.



## API Endpoints

### Books

- `GET /api/books` – List and search books.
- `POST /api/books` – Add new books and copies.

### Borrowing

- `POST /api/borrow` – Borrow a book copy.
- `POST /api/return` – Return a borrowed book.

### Borrowers

- `GET /api/borrowers` – List borrowers.
- `POST /api/borrowers` – Add a new borrower.
- `GET /api/borrowers/<id>` – View borrower details and loan history.
- `PUT /api/borrowers/<id>` – Update borrower info.

### Fines

- `POST /api/fines/pay` – Record a fine payment.

### Stats

- `GET /api/stats` – Library summary statistics.

