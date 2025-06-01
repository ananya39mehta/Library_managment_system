from sqlalchemy import create_engine, MetaData, Table, select
from pymongo import MongoClient
from datetime import datetime, date
import os
from decimal import Decimal

# ---------- Configuration ----------
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://lms:lms123@db:5432/library")
MONGO_URL = "mongodb://library_managment_system-mongo-1:27017/"
MONGO_DB = "library_db"

# ---------- Connect to PostgreSQL ----------
pg_engine = create_engine(POSTGRES_URL)
pg_conn = pg_engine.connect()
pg_metadata = MetaData()
pg_metadata.reflect(bind=pg_engine)

# ---------- Connect to MongoDB ----------
mongo_client = MongoClient(MONGO_URL)
mongo_db = mongo_client[MONGO_DB]

# ---------- Helper function to convert Decimal and date to MongoDB-compatible types ----------
def sanitize_for_mongo(obj):
    if isinstance(obj, dict):
        return {k: sanitize_for_mongo(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [sanitize_for_mongo(elem) for elem in obj]
    elif isinstance(obj, Decimal):
        return float(obj)
    elif isinstance(obj, date) and not isinstance(obj, datetime):
        return datetime(obj.year, obj.month, obj.day)
    return obj

# Note: Commented out the following lines to avoid wiping existing data on every run
# mongo_db.books.delete_many({})
# mongo_db.borrowers.delete_many({})
# mongo_db.loans.delete_many({})

# ---------- Migrate Books ----------
book_table = pg_metadata.tables["book"]
book_copy_table = pg_metadata.tables["book_copy"]
book_language_table = pg_metadata.tables["book_language"]
book_category_table = pg_metadata.tables["book_category"]
category_table = pg_metadata.tables["category"]

books = []
for book in pg_conn.execute(select(book_table)).fetchall():
    metadata_id = book.metadata_id

    # Get book copies
    copies = [
        sanitize_for_mongo(dict(copy._mapping))
        for copy in pg_conn.execute(
            select(book_copy_table).where(book_copy_table.c.metadata_id == metadata_id)
        ).fetchall()
    ]

    # Get languages
    languages = [
        row.language
        for row in pg_conn.execute(
            select(book_language_table).where(book_language_table.c.metadata_id == metadata_id)
        )
    ]

    # Get categories
    category_ids = [
        row.category_id
        for row in pg_conn.execute(
            select(book_category_table).where(book_category_table.c.metadata_id == metadata_id)
        )
    ]
    categories = [
        row.name
        for row in pg_conn.execute(
            select(category_table).where(category_table.c.category_id.in_(category_ids))
        )
    ]

    books.append({
        "metadata_id": metadata_id,
        "title": book.title,
        "author": book.author,
        "publisher": book.publisher,
        "isbn": book.isbn,
        "publication_year": book.publication_year,
        "edition": book.edition,
        "format": book.format,
        "languages": languages,
        "categories": categories,
        "copies": copies,
        "book_summary": []  # Initialize summaries as empty list
    })

# Upsert books to avoid duplicates if script reruns
for book in books:
    mongo_db.books.update_one(
        {"metadata_id": book["metadata_id"]},
        {"$setOnInsert": book},
        upsert=True
    )
print(f"Processed {len(books)} books into MongoDB.")

# ---------- Migrate Borrowers ----------
borrower_table = pg_metadata.tables["borrower"]
borrower_category_table = pg_metadata.tables["borrower_category"]
department_table = pg_metadata.tables["department"]

borrowers = []
for borrower in pg_conn.execute(select(borrower_table)).fetchall():
    # Get category
    category = pg_conn.execute(
        select(borrower_category_table).where(borrower_category_table.c.name == borrower.category_id)
    ).fetchone()

    # Get department
    dept = pg_conn.execute(
        select(department_table).where(department_table.c.dept_id == borrower.dept_id)
    ).fetchone()

    borrower_doc = {
        "borrower_id": borrower.borrower_id,
        "name": borrower.name,
        "email": borrower.email,
        "phone": borrower.phone,
        "address": borrower.address,
        "registration_date": borrower.registration_date.isoformat() if borrower.registration_date else None,
        "total_fines_due": float(borrower.total_fines_due or 0),
        "category": dict(category._mapping) if category else None,
        "department": dict(dept._mapping) if dept else None
    }

    borrowers.append(sanitize_for_mongo(borrower_doc))

# Upsert borrowers
for borrower in borrowers:
    mongo_db.borrowers.update_one(
        {"borrower_id": borrower["borrower_id"]},
        {"$setOnInsert": borrower},
        upsert=True
    )
print(f"Processed {len(borrowers)} borrowers into MongoDB.")

# ---------- Migrate Loans ----------
loan_table = pg_metadata.tables["loan"]
fine_table = pg_metadata.tables["fine_transaction"]

loans = []
for loan in pg_conn.execute(select(loan_table)).fetchall():
    # Get fine transactions
    fines = [
        sanitize_for_mongo(dict(fine._mapping))
        for fine in pg_conn.execute(
            select(fine_table).where(fine_table.c.loan_id == loan.loan_id)
        ).fetchall()
    ]

    loan_doc = {
        "loan_id": loan.loan_id,
        "borrower_id": loan.borrower_id,
        "book_id": loan.book_id,
        "checkout_date": loan.checkout_date.isoformat() if loan.checkout_date else None,
        "due_date": loan.due_date.isoformat() if loan.due_date else None,
        "return_date": loan.return_date.isoformat() if loan.return_date else None,
        "format_borrowed": loan.format_borrowed,
        "fine_amount": float(loan.fine_amount or 0),
        "status": loan.status,
        "fine_transactions": fines
    }

    loans.append(sanitize_for_mongo(loan_doc))

# Upsert loans
for loan in loans:
    mongo_db.loans.update_one(
        {"loan_id": loan["loan_id"]},
        {"$setOnInsert": loan},
        upsert=True
    )
print(f"Processed {len(loans)} loans into MongoDB.")

# ---------- Done ----------
print("✅ Migration complete.")
