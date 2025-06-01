# 📚 Library Book Summary Editor

This project is a simple web-based interface for managing and editing book summaries stored in a MongoDB database. It was built as part of an assignment to demonstrate basic CRUD operations, dynamic rendering with JavaScript, and thoughtful UI/UX using modals.

---

## ✨ What This Project Does

- Displays a table of library books retrieved from a MongoDB collection.
- Shows metadata like `metadata_id`, title, author, and current summary (if any).
- Lets you **edit or add summaries** for each book using a clean modal popup.
- Automatically updates MongoDB when a summary is saved.
- Keeps the experience smooth with real-time updates — no need to refresh manually.

---

## 🧠 Why I Built It

This assignment challenged me to integrate:
- Front-end development (HTML, CSS, JS)
- Working with APIs and async calls (`fetch`)
- Connecting to a backend powered by MongoDB
- Implementing a modal-based UI that feels intuitive and functional

The goal wasn’t just to display data, but to give users a better way to interact with it — especially editing multiline summaries in a clear, user-friendly way.

---

## ⚙️ How It Works

### 📦 Backend (Expected API)

This project assumes the existence of a REST API with the following endpoints:

- `GET /mongo/books`: returns a list of all books
- `POST /mongo/books/:metadata_id/summary`: updates the summary of a book

Each book in the response is expected to have:
```json
{
  "metadata_id": 1,
  "title": "1984",
  "author": "George Orwell",
  "book_summary": ["this is a book"]
}
