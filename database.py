import sqlite3

def setup():    
    global conn 
    global cursor
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS match_2 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS minesweeper (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS simon_says (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")

# cursor.execute("INSERT INTO match_2 (name, score) VALUES (?, ?)", ('sigma', 123.4))

def get_match_2_scores():
    leaderboard = []
    cursor.execute("SELECT * FROM match_2 ORDER BY score ASC")
    data = cursor.fetchall()
    for i, d in enumerate(data):
        leaderboard.append((i + 1, d[1], d[2]))
    return leaderboard

def add_match_2_scores(data):
    cursor.execute("INSERT INTO match_2 (name, score) VALUES (?, ?)", (data[0], data[1]))

def close():
    conn.commit()
    conn.close()