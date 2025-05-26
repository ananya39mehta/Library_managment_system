# Library Management System API

This is a Flask-based backend service for a Library Management System that allows for managing books, borrowers, loans, fines, and related entities.

## Features

- **Book Management**: Add, search, and list books with copies, languages, and categories.
- **Borrowing System**: Record borrowing and returning of book copies, with automatic due dates and fine calculation.
- **Fine Handling**: Calculate and record fines and payments.
- **Borrower Management**: Add, update, and view borrower information including loan history and fines.
- **Statistics Endpoint**: Fetch summary statistics like total books, active loans, and overdue books.

## Notable Design and Implementation Decisions

- **Normalized Relational Schema**: The system uses normalized SQLAlchemy models, including many-to-many relationships (e.g., books and categories) and one-to-many (e.g., borrowers and loans).
- **ISBN-Based Metadata Deduplication**: New books are deduplicated by ISBN; only new copies are added if the ISBN exists.
- **Fine Calculation on Return**: Fines are dynamically calculated at the time of return using category-specific daily rates.
- **Efficient Loan Lookup**: Book availability and borrower loans are optimized using eager loading and indexed queries.
- **CORS Enabled**: The backend supports CORS for front-end integrations.
- **Structured JSON API**: Routes follow REST-like semantics and return well-structured JSON for frontend consumption.

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

