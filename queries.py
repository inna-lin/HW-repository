import sqlite3

# Підключення до бази даних
conn = sqlite3.connect("my_database.db")
cursor = conn.cursor()

# З А П И Т И

# Отримати всі завдання певного користувача
user_id = 1
cursor.execute("SELECT * FROM tasks WHERE user_id = ?", (user_id,))
tasks_for_user = cursor.fetchall()

# Отримати завдання за певним статусом
status_name = 'new'
cursor.execute(
    "SELECT * FROM tasks WHERE status_id = (SELECT id FROM status WHERE name = ?)",
    (status_name,)
)
tasks_by_status = cursor.fetchall()

# Оновити статус завдання
task_id = 1
new_status = 'in progress'
cursor.execute(
    "UPDATE tasks SET status_id = (SELECT id FROM status WHERE name = ?) WHERE id = ?",
    (new_status, task_id)
)
conn.commit()

# Отримати користувачів без завдань
cursor.execute(
    "SELECT * FROM users WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks)"
)
users_without_tasks = cursor.fetchall()

# Додати нове завдання
title = 'Нове завдання'
description = 'Опис завдання'
status_name = 'new'
user_id = 2
cursor.execute(
    "INSERT INTO tasks (title, description, status_id, user_id) VALUES (?, ?, (SELECT id FROM status WHERE name = ?), ?)",
    (title, description, status_name, user_id)
)
conn.commit()

# Завершення
conn.close()
