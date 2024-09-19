import sqlite3

def create_database():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    ''')

    # Add some initial users
    initial_users = [
        ('John Doe', 'john@example.com'),
        ('Jane Smith', 'jane@example.com'),
        ('Bob Johnson', 'bob@example.com'),
    ]

    cursor.executemany('INSERT OR IGNORE INTO users (name, email) VALUES (?, ?)', initial_users)

    conn.commit()
    conn.close()

if __name__ == '__main__':
    create_database()
    print("Database created and initialized with users.")