import sqlite3

MAX_SCORES = 6

def init():    
    global conn 
    global cursor
    conn = sqlite3.connect('game_data.db')
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS match_2 (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS minesweeper (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")
    cursor.execute("CREATE TABLE IF NOT EXISTS simon_says (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, score REAL)")

# cursor.execute("INSERT INTO match_2 (name, score) VALUES (?, ?)", ('sigma', 123.4))

# you can't pass table name as variable, so i just made a lot of functions

# match 2
def get_match_2_scores():
    leaderboard = []
    conn.commit()
    cursor.execute("SELECT * FROM match_2 ORDER BY score ASC")
    data = cursor.fetchall()
    for i, d in enumerate(data):
        leaderboard.append((i + 1, d[1], d[2]))
    return leaderboard

def add_match_2_score(data):
    cursor.execute("SELECT COUNT(*) FROM match_2")
    number_scores = cursor.fetchone()
    cursor.execute("INSERT INTO match_2 (name, score) VALUES (?, ?)", (data[0], data[1]))

    if number_scores[0] >= MAX_SCORES:
        cursor.execute("""DELETE FROM match_2 WHERE id = (select * from (
                        SELECT id FROM match_2 ORDER BY score ASC limit 6,1) AS t)""")
    conn.commit()

def is_better_match_2(score):
    cursor.execute("SELECT COUNT(*) FROM match_2")
    number_scores = cursor.fetchone()
    if number_scores[0] < MAX_SCORES:
        return True
    cursor.execute("SELECT MAX(score) FROM match_2") # the bigger time the worse
    min_score = cursor.fetchone()
    return score < min_score

# simon says
def get_simon_says_scores():
    leaderboard = []
    conn.commit()
    cursor.execute("SELECT * FROM simon_says ORDER BY score DESC")
    data = cursor.fetchall()
    for i, d in enumerate(data):
        leaderboard.append((i + 1, d[1], d[2]))
    return leaderboard

def add_simon_says_score(data):
    cursor.execute("SELECT COUNT(*) FROM simon_says")
    number_scores = cursor.fetchone()
    cursor.execute("INSERT INTO simon_says (name, score) VALUES (?, ?)", (data[0], data[1]))

    if number_scores[0] >= MAX_SCORES:
        cursor.execute("""DELETE FROM simon_says WHERE id = (select * from (
                        SELECT id FROM simon_says ORDER BY score DESC limit 6,1) AS t)""")
    conn.commit()

def is_better_simon_says(score):
    cursor.execute("SELECT COUNT(*) FROM simon_says")
    number_scores = cursor.fetchone()
    if number_scores[0] < MAX_SCORES:
        return True
    cursor.execute("SELECT MIN(score) FROM simon_says") # the smaller score the worse
    min_score = cursor.fetchone()
    print(min_score)
    return score > min_score

# minesweeper
def get_minesweeper_scores():
    leaderboard = []
    conn.commit()
    cursor.execute("SELECT * FROM minesweeper ORDER BY score ASC")
    data = cursor.fetchall()
    for i, d in enumerate(data):
        leaderboard.append((i + 1, d[1], d[2]))
    return leaderboard

def add_minesweeper_score(data):
    cursor.execute("SELECT COUNT(*) FROM minesweeper")
    number_scores = cursor.fetchone()
    cursor.execute("INSERT INTO minesweeper (name, score) VALUES (?, ?)", (data[0], data[1]))

    if number_scores[0] >= MAX_SCORES:
        cursor.execute("""DELETE FROM minesweeper WHERE id = (select * from (
                        SELECT id FROM minesweeper ORDER BY score ASC limit 6,1) AS t)""")
    cursor.execute("SELECT * FROM minesweeper ORDER BY score ASC")
    data = cursor.fetchall()
    for i, d in enumerate(data):
        print((i + 1, d[1], d[2]))
    conn.commit()

def is_better_minesweeper(score):
    cursor.execute("SELECT COUNT(*) FROM minesweeper")
    number_scores = cursor.fetchone()
    if number_scores[0] < MAX_SCORES:
        return True
    cursor.execute("SELECT MAX(score) FROM minesweeper") # the bigger time the worse
    min_score = cursor.fetchone()
    return score < min_score[0]

def close():
    conn.commit()
    conn.close()

def clean_db():
    cursor.execute("DROP TABLE match_2")
    cursor.execute("DROP TABLE simon_says")
    cursor.execute("DROP TABLE minesweeper")