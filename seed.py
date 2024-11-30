import sqlite3
from faker import Faker
import random

# Підключення до бази даних
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# Створення таблиць
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    fullname VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(50) UNIQUE NOT NULL
);
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(100) NOT NULL,
    description TEXT,
    status_id INTEGER,
    user_id INTEGER,
    FOREIGN KEY (status_id) REFERENCES status (id),
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);
""")

# Наповнення таблиць
statuses = [('new',), ('in progress',), ('completed',)]
cursor.executemany("INSERT OR IGNORE INTO status (name) VALUES (?)", statuses)

faker = Faker()
users = [(faker.name(), faker.unique.email()) for _ in range(10)]
cursor.executemany("INSERT INTO users (fullname, email) VALUES (?, ?)", users)

user_ids = [row[0] for row in cursor.execute("SELECT id FROM users").fetchall()]
status_ids = [row[0] for row in cursor.execute("SELECT id FROM status").fetchall()]
tasks = [
    (
        faker.sentence(nb_words=5),
        faker.text(max_nb_chars=50),
        random.choice(status_ids),
        random.choice(user_ids),
    )
    for _ in range(20)
]
cursor.executemany(
    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, ?, ?)",
    tasks,
)

# Завершення
conn.commit()
conn.close()