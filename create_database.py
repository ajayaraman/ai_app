import sqlite3
import random

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # Drop the existing table if it exists
    cursor.execute('DROP TABLE IF EXISTS users')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        status TEXT NOT NULL
    )
    ''')

    # Add some initial users with random status
    initial_users = [
        ('John Doe', 'john@example.com', random.choice(['Online', 'Away', 'Not Available'])),
        ('Jane Smith', 'jane@example.com', random.choice(['Online', 'Away', 'Not Available'])),
        ('Bob Johnson', 'bob@example.com', random.choice(['Online', 'Away', 'Not Available'])),
        ('Alice Brown', 'alice@example.com', random.choice(['Online', 'Away', 'Not Available'])),
        ('Charlie Davis', 'charlie@example.com', random.choice(['Online', 'Away', 'Not Available'])),
    ]

    cursor.executemany('INSERT OR IGNORE INTO users (name, email, status) VALUES (?, ?, ?)', initial_users)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database created and initialized with users and their statuses.")