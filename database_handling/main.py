"""
database_handling.py
----------------------
A tour of Python database connectivity, with RUNNABLE examples using
sqlite3 (Python's built-in, file-based SQL database - no server required),
plus a Bank Management System project at the end.

WHY SQLITE FOR THE DEMOS:
MySQL, PostgreSQL, and MongoDB all require a running server to connect to,
so genuinely runnable end-to-end examples for them aren't possible without
one. sqlite3 uses the exact same connect -> cursor -> execute -> commit
pattern as MySQL/PostgreSQL, so everything you learn here transfers
directly. Reference snippets for MySQL, PostgreSQL, and MongoDB are
included further down (clearly marked as NOT executed) so you can see the
real syntax and swap them in once you have a server + credentials.

Run this file directly:
    python database_handling.py
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "demo.db"


# ---------------------------------------------------------------------------
# 1 & 2. CONNECTING, CURSORS, EXECUTE, COMMIT
# (This pattern is essentially identical across sqlite3, MySQL, and
#  PostgreSQL connector libraries - only the connect() call differs.)
# ---------------------------------------------------------------------------
def demo_connection_basics():
    print("\n=== CONNECTING & RUNNING QUERIES ===")

    # connect() opens (or creates) the database file
    conn = sqlite3.connect(DB_PATH)
    # a cursor is what you use to execute SQL statements
    cursor = conn.cursor()

    # CREATE TABLE - IF NOT EXISTS makes this safe to re-run
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            grade REAL NOT NULL
        )
    """)

    # commit() saves changes - without it, changes can be lost / not visible
    conn.commit()
    print("Table 'students' ready.")

    cursor.close()
    conn.close()  # always close the connection when done


# ---------------------------------------------------------------------------
# INSERTING DATA (with parameterized queries - never use string formatting
# for SQL values, it opens the door to SQL injection)
# ---------------------------------------------------------------------------
def demo_insert_data():
    print("\n=== INSERTING DATA ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear out old demo data so re-running this file gives consistent output
    cursor.execute("DELETE FROM students")

    students = [
        ("Ada Lovelace", 95.5),
        ("Grace Hopper", 98.0),
        ("Alan Turing", 92.3),
    ]

    # The ? placeholders are filled in safely by sqlite3 - this is what
    # protects against SQL injection (never do f"...{name}..." in SQL!)
    cursor.executemany(
        "INSERT INTO students (name, grade) VALUES (?, ?)", students
    )

    conn.commit()
    print(f"Inserted {cursor.rowcount if cursor.rowcount != -1 else len(students)} rows.")

    cursor.close()
    conn.close()


# ---------------------------------------------------------------------------
# READING DATA
# ---------------------------------------------------------------------------
def demo_read_data():
    print("\n=== READING DATA ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT id, name, grade FROM students ORDER BY grade DESC")
    rows = cursor.fetchall()  # fetchall() gets every matching row as a list of tuples
    print("All students, best grade first:")
    for row in rows:
        print(" ", row)

    # fetchone() gets just the next single row
    cursor.execute("SELECT name, grade FROM students WHERE grade > ?", (95,))
    top_student = cursor.fetchone()
    print("First student above 95:", top_student)

    cursor.close()
    conn.close()


# ---------------------------------------------------------------------------
# UPDATING & DELETING DATA
# ---------------------------------------------------------------------------
def demo_update_and_delete():
    print("\n=== UPDATING & DELETING DATA ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET grade = ? WHERE name = ?", (99.0, "Ada Lovelace")
    )
    conn.commit()
    print(f"Updated {cursor.rowcount} row(s).")

    cursor.execute("SELECT name, grade FROM students WHERE name = ?", ("Ada Lovelace",))
    print("After update:", cursor.fetchone())

    cursor.execute("DELETE FROM students WHERE name = ?", ("Alan Turing",))
    conn.commit()
    print(f"Deleted {cursor.rowcount} row(s).")

    cursor.execute("SELECT name FROM students")
    print("Remaining students:", [row[0] for row in cursor.fetchall()])

    cursor.close()
    conn.close()


# ---------------------------------------------------------------------------
# ERROR HANDLING WITH DATABASES
# Combine this with what you learned in exception_handling.py
# ---------------------------------------------------------------------------
def demo_database_error_handling():
    print("\n=== DATABASE ERROR HANDLING ===")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    try:
        # Deliberately broken SQL to demonstrate catching a database error
        cursor.execute("SELECT * FROM a_table_that_does_not_exist")
    except sqlite3.OperationalError as e:
        print("Caught database error:", e)
    finally:
        cursor.close()
        conn.close()


# ---------------------------------------------------------------------------
# REFERENCE ONLY - NOT EXECUTED
# The same connect -> cursor -> execute -> commit pattern, shown for
# MySQL, PostgreSQL, and MongoDB. These require an actual server and
# credentials, so they're kept as commented reference code.
# ---------------------------------------------------------------------------
"""
--- MySQL (pip install mysql-connector-python) ---

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    database="your_database",
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()


--- PostgreSQL (pip install psycopg2-binary) ---

import psycopg2

conn = psycopg2.connect(
    host="localhost",
    user="your_username",
    password="your_password",
    dbname="your_database",
)
cursor = conn.cursor()
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()
conn.commit()
cursor.close()
conn.close()


--- MongoDB (pip install pymongo) ---
# MongoDB is NoSQL - no tables/SQL, instead you work with collections
# of JSON-like documents.

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017/")
db = client["your_database"]
students = db["students"]

students.insert_one({"name": "Ada Lovelace", "grade": 95.5})
top_students = students.find({"grade": {"$gt": 95}})
for s in top_students:
    print(s)

students.update_one({"name": "Ada Lovelace"}, {"$set": {"grade": 99.0}})
students.delete_one({"name": "Alan Turing"})
"""


# ---------------------------------------------------------------------------
# PROJECT: Bank Management System (SQLite-backed)
# CRUD operations wrapped in a class, with parameterized queries and
# error handling - the same shape you'd use with MySQL/PostgreSQL.
# ---------------------------------------------------------------------------
class InsufficientFundsError(Exception):
    pass


class BankManagementSystem:
    def __init__(self, db_path):
        self.conn = sqlite3.connect(db_path)
        self._create_table()

    def _create_table(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS accounts (
                account_id INTEGER PRIMARY KEY AUTOINCREMENT,
                owner TEXT NOT NULL,
                balance REAL NOT NULL DEFAULT 0
            )
        """)
        self.conn.commit()

    # --- CREATE ---
    def open_account(self, owner, initial_deposit=0.0):
        cursor = self.conn.execute(
            "INSERT INTO accounts (owner, balance) VALUES (?, ?)",
            (owner, initial_deposit),
        )
        self.conn.commit()
        return cursor.lastrowid  # the new account's auto-generated id

    # --- READ ---
    def get_account(self, account_id):
        cursor = self.conn.execute(
            "SELECT account_id, owner, balance FROM accounts WHERE account_id = ?",
            (account_id,),
        )
        return cursor.fetchone()

    def list_accounts(self):
        cursor = self.conn.execute("SELECT account_id, owner, balance FROM accounts")
        return cursor.fetchall()

    # --- UPDATE ---
    def deposit(self, account_id, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be positive.")
        self.conn.execute(
            "UPDATE accounts SET balance = balance + ? WHERE account_id = ?",
            (amount, account_id),
        )
        self.conn.commit()

    def withdraw(self, account_id, amount):
        if amount <= 0:
            raise ValueError("Withdrawal amount must be positive.")
        account = self.get_account(account_id)
        if account is None:
            raise ValueError(f"No account with id {account_id}")
        _, _, balance = account
        if amount > balance:
            raise InsufficientFundsError(
                f"Cannot withdraw {amount:.2f}; balance is {balance:.2f}"
            )
        self.conn.execute(
            "UPDATE accounts SET balance = balance - ? WHERE account_id = ?",
            (amount, account_id),
        )
        self.conn.commit()

    # --- DELETE ---
    def close_account(self, account_id):
        cursor = self.conn.execute(
            "DELETE FROM accounts WHERE account_id = ?", (account_id,)
        )
        self.conn.commit()
        return cursor.rowcount > 0  # True if a row was actually deleted

    def close(self):
        self.conn.close()


def demo_bank_management_system():
    print("\n=== PROJECT: BANK MANAGEMENT SYSTEM ===")
    bank_db_path = Path(__file__).parent / "bank_demo.db"
    bank = BankManagementSystem(bank_db_path)

    # Reset for a clean, repeatable demo run
    bank.conn.execute("DELETE FROM accounts")
    bank.conn.commit()

    ada_id = bank.open_account("Ada Lovelace", initial_deposit=500)
    grace_id = bank.open_account("Grace Hopper", initial_deposit=1000)
    print(f"Opened accounts: Ada={ada_id}, Grace={grace_id}")

    bank.deposit(ada_id, 250)
    bank.withdraw(grace_id, 300)
    print("Ada's account:", bank.get_account(ada_id))
    print("Grace's account:", bank.get_account(grace_id))

    try:
        bank.withdraw(ada_id, 10000)
    except InsufficientFundsError as e:
        print("Error:", e)

    print("All accounts:", bank.list_accounts())

    closed = bank.close_account(grace_id)
    print(f"Closed Grace's account? {closed}")
    print("Remaining accounts:", bank.list_accounts())

    bank.close()


# ---------------------------------------------------------------------------
if __name__ == "__main__":
    demo_connection_basics()
    demo_insert_data()
    demo_read_data()
    demo_update_and_delete()
    demo_database_error_handling()
    demo_bank_management_system()
    print(f"\nSQLite demo databases created at: {DB_PATH.parent}")