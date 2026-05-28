import sqlite3

conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Economy table
cursor.execute("""
CREATE TABLE IF NOT EXISTS economy (
    user_id INTEGER PRIMARY KEY,
    coins INTEGER DEFAULT 0,
    xp INTEGER DEFAULT 0,
    level INTEGER DEFAULT 1
)
""")
# Inventory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS inventory (
    user_id INTEGER,
    item TEXT,
    amount INTEGER,
    PRIMARY KEY(user_id, item)
)
""")
# Warnings table
cursor.execute("""
CREATE TABLE IF NOT EXISTS warnings (
    user_id INTEGER,
    moderator_id INTEGER,
    reason TEXT
)
""")
# Hospitality table
cursor.execute("""
CREATE TABLE IF NOT EXISTS hospitality (
    user_id INTEGER PRIMARY KEY,
    points INTEGER DEFAULT 0
)
""")
# Shop table
cursor.execute("""
CREATE TABLE IF NOT EXISTS shop (
    item TEXT PRIMARY KEY,
    price INTEGER
)
""")
# Default shop items
items = [
    ("cookie", 100),
    ("vip", 500),
    ("waffle_box", 300)
]

for item in items:
    cursor.execute(
        "INSERT OR IGNORE INTO shop (item, price) VALUES (?, ?)",
        item
    )
    # Memory table
cursor.execute("""
CREATE TABLE IF NOT EXISTS memory (
    user_id INTEGER,
    fact TEXT
)
""")
conn.commit()
conn.close()