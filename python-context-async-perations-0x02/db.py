import sqlite3

db = sqlite3.connect('example.db')
try:
    print('Connected to the example database.')

    # Add the 'age' column to the 'users' table
    try:
        db.execute('ALTER TABLE users ADD COLUMN age INTEGER')
        print('Successfully added age column to users table')
    except sqlite3.OperationalError as err:
        print('Error adding age column:', err)

    # Insert sample data
    users = [
        ("Alice", "alice@example.com", 30),
        ("Bob", "bob@example.com", 25),
        ("Charlie", "charlie@example.com", 35),
        ("David", "david@example.com", 22)
    ]

    stmt = db.cursor()
    for user in users:
        try:
            stmt.execute(
                'INSERT INTO users (name, email, age) VALUES (?, ?, ?)', user)
            print('Inserted user:', user[0])
        except sqlite3.IntegrityError as err:
            print('Error inserting user:', err)

    db.commit()
finally:
    db.close()
    print('Closed the database connection.')
