import sys
import sqlite3

from PySide6.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QListWidget,
    QLineEdit,
    QTextEdit,
    QPushButton,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)


class Database:
    def __init__(self, database_name="notes.db"):
        self.connection = sqlite3.connect(database_name)
        self.create_table()

    def create_table(self):
        self.connection.execute("""
            CREATE TABLE IF NOT EXISTS notes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                content TEXT NOT NULL
            )
        """)
        self.connection.commit()

    def get_notes(self):
        cursor = self.connection.execute("""
            SELECT id, title
            FROM notes
            ORDER BY id DESC
        """)

        return cursor.fetchall()

    def get_note(self, note_id):
        cursor = self.connection.execute("""
            SELECT title, content
            FROM notes
            WHERE id = ?
        """, (note_id,))

        return cursor.fetchone()

    def create_note(self, title, content):
        cursor = self.connection.execute("""
            INSERT INTO notes (title, content)
            VALUES (?, ?)
        """, (title, content))

        self.connection.commit()

        return cursor.lastrowid

    def update_note(self, note_id, title, content):
        self.connection.execute("""
            UPDATE notes
            SET title = ?, content = ?
            WHERE id = ?
        """, (title, content, note_id))

        self.connection.commit()

    def delete_note(self, note_id):
        self.connection.execute("""
            DELETE FROM notes
            WHERE id = ?
        """, (note_id,))

        self.connection.commit()

    def close(self):
        self.connection.close()


class NotesWindow(QMainWindow):

    def __init__(self):
        super().__init__()

        self.setWindowTitle("Notes")
        self.resize(800, 500)

        self.database = Database()

        # Currently selected note
        self.current_note_id = None

        self.create_ui()
        self.load_notes()

    def create_ui(self):

        # =========================
        # LEFT SIDE
        # =========================

        self.notes_list = QListWidget()

        self.new_button = QPushButton("New")
        self.delete_button = QPushButton("Delete")

        left_layout = QVBoxLayout()

        left_layout.addWidget(QLabel("Notes"))
        left_layout.addWidget(self.notes_list)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.new_button)
        button_layout.addWidget(self.delete_button)

        left_layout.addLayout(button_layout)

        left_widget = QWidget()
        left_widget.setLayout(left_layout)

        # =========================
        # RIGHT SIDE
        # =========================

        self.title_edit = QLineEdit()
        self.title_edit.setPlaceholderText("Note title")

        self.content_edit = QTextEdit()
        self.content_edit.setPlaceholderText("Write your note here...")

        self.save_button = QPushButton("Save")

        right_layout = QVBoxLayout()

        right_layout.addWidget(self.title_edit)
        right_layout.addWidget(self.content_edit)
        right_layout.addWidget(self.save_button)

        right_widget = QWidget()
        right_widget.setLayout(right_layout)

        # =========================
        # MAIN LAYOUT
        # =========================

        main_layout = QHBoxLayout()

        main_layout.addWidget(left_widget, 1)
        main_layout.addWidget(right_widget, 2)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

        # =========================
        # SIGNALS
        # =========================

        self.notes_list.currentRowChanged.connect(
            self.note_selected
        )

        self.new_button.clicked.connect(
            self.new_note
        )

        self.save_button.clicked.connect(
            self.save_note
        )

        self.delete_button.clicked.connect(
            self.delete_note
        )

    # ==================================
    # LOAD NOTES
    # ==================================

    def load_notes(self):

        self.notes_list.clear()

        notes = self.database.get_notes()

        for note_id, title in notes:

            display_title = title if title else "(Untitled)"

            self.notes_list.addItem(display_title)

            item = self.notes_list.item(
                self.notes_list.count() - 1
            )

            # Store database ID inside the QListWidgetItem
            item.setData(256, note_id)

    # ==================================
    # SELECT NOTE
    # ==================================

    def note_selected(self, row):

        if row < 0:
            return

        item = self.notes_list.item(row)

        note_id = item.data(256)

        note = self.database.get_note(note_id)

        if note is None:
            return

        title, content = note

        self.current_note_id = note_id

        self.title_edit.setText(title)
        self.content_edit.setPlainText(content)

    # ==================================
    # NEW NOTE
    # ==================================

    def new_note(self):

        self.current_note_id = None

        self.notes_list.clearSelection()

        self.title_edit.clear()
        self.content_edit.clear()

        self.title_edit.setFocus()

    # ==================================
    # SAVE NOTE
    # ==================================

    def save_note(self):

        title = self.title_edit.text().strip()
        content = self.content_edit.toPlainText()

        if not title:
            QMessageBox.warning(
                self,
                "Missing title",
                "Please enter a title."
            )
            return

        # Creating a new note
        if self.current_note_id is None:

            note_id = self.database.create_note(
                title,
                content
            )

            self.current_note_id = note_id

        # Updating existing note
        else:

            self.database.update_note(
                self.current_note_id,
                title,
                content
            )

        self.load_notes()

        # Re-select saved note
        for row in range(self.notes_list.count()):

            item = self.notes_list.item(row)

            if item.data(256) == self.current_note_id:

                self.notes_list.setCurrentRow(row)
                break

    # ==================================
    # DELETE NOTE
    # ==================================

    def delete_note(self):

        if self.current_note_id is None:
            return

        answer = QMessageBox.question(
            self,
            "Delete Note",
            "Are you sure you want to delete this note?"
        )

        if answer != QMessageBox.StandardButton.Yes:
            return

        self.database.delete_note(
            self.current_note_id
        )

        self.current_note_id = None

        self.title_edit.clear()
        self.content_edit.clear()

        self.load_notes()

    # ==================================
    # CLOSE
    # ==================================

    def closeEvent(self, event):

        self.database.close()

        event.accept()


def main():

    app = QApplication(sys.argv)

    window = NotesWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
