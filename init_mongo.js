// Switch to or create the database
db = db.getSiblingDB('library_db');

// ----------------------
// Books Collection
// ----------------------
db.books.insertMany([
  {
    metadata_id: 1,
    title: "1984",
    author: "George Orwell",
    publisher: "Secker & Warburg",
    isbn: "9780451524935",
    publication_year: 1949,
    edition: "1st",
    format: "Hardcover",
    languages: ["English"],
    categories: ["Fiction", "Dystopia"],
    copies: [
      { book_id: 101, shelf_location: "A1", available: true },
      { book_id: 102, shelf_location: "A2", available: false }
    ],
    book_summary: ["this is a book "]
  }
]);

// ----------------------
// Borrowers Collection
// ----------------------
db.borrowers.insertMany([
  {
    borrower_id: 1001,
    name: "John Doe",
    email: "john.doe@example.com",
    phone: "1234567890",
    address: "123 Main Street",
    registration_date: new Date("2023-01-15"),
    category: {
      name: "student",
      requires_department: true,
      max_books_allowed: 5,
      max_loan_period: 14,
      fine_rate_per_day: 2.00
    },
    department: {
      dept_id: 1,
      name: "Computer Science",
      building: "Block A",
      contact_number: "9876543210"
    },
    total_fines_due: 5.00
  }
]);

// ----------------------
// Loans Collection
// ----------------------
db.loans.insertMany([
  {
    loan_id: 5001,
    borrower_id: 1001,
    book_id: 102,
    checkout_date: new Date("2024-04-01"),
    due_date: new Date("2024-04-15"),
    return_date: new Date("2024-04-20"),
    format_borrowed: "Hardcover",
    fine_amount: 5.00,
    status: "returned",
    fine_transactions: [
      {
        transaction_id: 1,
        amount: 5.00,
        payment_date: new Date("2024-04-21"),
        payment_method: "Credit Card"
      }
    ]
  }
]);

// ----------------------
// Optional Indexes
// ----------------------
db.books.createIndex({ title: "text", author: "text", isbn: "text" });
db.borrowers.createIndex({ email: 1 }, { unique: true });
