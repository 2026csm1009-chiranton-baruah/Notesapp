# PySide6 Notes App

A simple desktop **Notes application** built with **Python, PySide6, and SQLite3**.

The application provides a graphical interface for creating, viewing, editing, and deleting notes. Notes are stored persistently in a local SQLite database, so they remain available after the application is closed and reopened.

---

## Features

- Create new notes
- Give notes a title
- Write and edit note content
- View all saved notes
- Select a note from the notes list
- Update existing notes
- Delete notes
- Persistent local storage using SQLite
- Simple desktop GUI using PySide6

---

## Technologies Used

### Python

The application is written in Python.

### PySide6

[PySide6](https://doc.qt.io/qtforpython/) provides Python bindings for Qt 6 and is used to create the graphical user interface.

The application uses several Qt widgets, including:

- `QMainWindow`
- `QWidget`
- `QListWidget`
- `QLineEdit`
- `QTextEdit`
- `QPushButton`
- `QMessageBox`
- `QVBoxLayout`
- `QHBoxLayout`

### SQLite3

Python's built-in `sqlite3` module is used for persistent data storage.

No separate SQLite installation is required.

---

## Project Structure

A minimal version of the project looks like this:

```text
notes-app/
│
├── notes.py
├── notes.db
└── README.md
```

### `notes.py`

Contains the complete application.

It includes:

- SQLite database handling
- GUI creation
- Note creation
- Note selection
- Note editing
- Note deletion
- Application event handling

### `notes.db`

The SQLite database containing the saved notes.

This file is automatically created the first time the application is run.

### `README.md`

Documentation for the project.

---

## Requirements

You need:

- Python 3.9 or newer
- PySide6

SQLite3 is included with Python.

You can check your Python installation with:

```bash
python --version
```

On some systems you may need:

```bash
python3 --version
```

---

## Installation

### 1. Clone or download the project

If the project is hosted in a Git repository:

```bash
git clone <repository-url>
cd notes-app
```

Alternatively, simply place `notes.py` in a directory of your choice.

---

### 2. Install PySide6

Run:

```bash
pip install PySide6
```

If your system uses `pip3`:

```bash
pip3 install PySide6
```

You can verify the installation with:

```bash
python -c "import PySide6; print(PySide6.__version__)"
```

---

## Running the Application

From the project directory, run:

```bash
python notes.py
```

or:

```bash
python3 notes.py
```

The Notes application window should appear.

If `notes.db` does not already exist, the application automatically creates it.

---

# Using the Application

## Creating a Note

1. Click **New**.
2. Enter a title in the title field.
3. Enter your note in the text editor.
4. Click **Save**.

The note will appear in the list on the left.

Example:

```text
Title:
Shopping List

Content:
- Milk
- Bread
- Eggs
```

---

## Opening a Note

Click a note in the list on the left.

Its title and contents will appear in the editor on the right.

---

## Editing a Note

1. Select the note you want to edit.
2. Modify the title or content.
3. Click **Save**.

The existing database entry will be updated.

---

## Deleting a Note

1. Select the note.
2. Click **Delete**.
3. Confirm the deletion.

The note will be permanently removed from the SQLite database.

---

## Creating Another Note

Click **New**.

The editor will be cleared and you can enter another note.

---

# Database

The application uses SQLite for storage.

The database file is:

```text
notes.db
```

The database contains a table called `notes`:

```sql
CREATE TABLE IF NOT EXISTS notes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    content TEXT NOT NULL
);
```

The table therefore has three columns:

| Column | Type | Description |
|---|---|---|
| `id` | INTEGER | Unique ID for each note |
| `title` | TEXT | Note title |
| `content` | TEXT | Note contents |

---

## Database Persistence

The database is stored locally in the project directory.

For example:

```text
notes-app/
├── notes.py
├── notes.db
└── README.md
```

Closing the application does **not** delete the notes.

When the application is started again, it reads the existing database and loads the saved notes.

---

# How the Application Works

The application has two major components.

```text
┌───────────────────────────────┐
│          PySide6 GUI          │
│                               │
│  ┌──────────┐  ┌───────────┐ │
│  │ Note List│  │   Editor  │ │
│  │          │  │           │ │
│  │ Note 1   │  │ Title     │ │
│  │ Note 2   │  │           │ │
│  │ Note 3   │  │ Content   │ │
│  └──────────┘  └───────────┘ │
└───────────────┬───────────────┘
                │
                ▼
       ┌─────────────────┐
       │    Database     │
       │                 │
       │    SQLite3      │
       │    notes.db     │
       └─────────────────┘
```

### GUI

PySide6 handles:

- Windows
- Buttons
- Text fields
- Note list
- User interaction
- Signals and slots

### Database

SQLite handles:

- Storing notes
- Retrieving notes
- Updating notes
- Deleting notes

---

# Application Architecture

The application is divided conceptually into two parts.

## `Database`

The `Database` class handles SQLite operations.

Important methods include:

```python
create_table()
get_notes()
get_note()
create_note()
update_note()
delete_note()
close()
```

This keeps database operations separate from most of the GUI code.

---

## `NotesWindow`

The `NotesWindow` class handles the user interface.

Important methods include:

```python
create_ui()
load_notes()
note_selected()
new_note()
save_note()
delete_note()
closeEvent()
```

The GUI communicates with the database through the `Database` object.

---

# Signals and Slots

PySide6 uses Qt's **signals and slots** mechanism to respond to user actions.

For example:

```python
self.new_button.clicked.connect(
    self.new_note
)
```

means:

```text
User clicks New
       ↓
clicked signal
       ↓
new_note()
       ↓
Editor is cleared
```

Similarly:

```python
self.save_button.clicked.connect(
    self.save_note
)
```

connects the Save button to the function responsible for inserting or updating the database.

---

# Troubleshooting

## `ModuleNotFoundError: No module named 'PySide6'`

Install PySide6:

```bash
pip install PySide6
```

If that does not work, try:

```bash
python -m pip install PySide6
```

---

## Python command is not recognized

Try:

```bash
python3 notes.py
```

instead of:

```bash
python notes.py
```

On Windows, make sure Python has been added to PATH.

---

## Database is empty

If `notes.db` has no notes, simply create one using the **New** button and click **Save**.

The database is populated automatically.

---

## Resetting the application

To completely erase all saved notes, close the application and delete:

```text
notes.db
```

Then start the application again.

A new empty database will be created automatically.

**Warning:** deleting `notes.db` permanently deletes all notes stored in it.

---

# Future Improvements

Possible extensions for future versions include:

- Search notes
- Note timestamps
- Automatic saving
- Keyboard shortcuts
- Dark mode
- Rich-text editing
- Note categories/tags
- Pinning important notes
- Sorting notes
- Database backup/export
- Import/export notes
- Markdown support
- Better application styling
- Proper Qt `UserRole` usage instead of a numeric item-data role
- Separation into multiple Python modules
- Packaging the application as an executable

---

## License

This project is intended as a learning project for experimenting with **PySide6 GUI development and SQLite database programming**.