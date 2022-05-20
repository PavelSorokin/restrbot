import sqlite3
import logging
conn = sqlite3.connect("restoran2.db", check_same_thread=False)
log = logging.getLogger(__name__)
log.debug("Trying to connect to database.sqlite or create new if not exist")
with conn:
#    log.debug("Initializing cursor")
    cursor = conn.cursor()   

    cursor.executescript("""CREATE TABLE IF NOT EXISTS users 
        (
            chat_id    INTEGER  PRIMARY KEY,
            username   VARCHAR,
            first_name VARCHAR,
            last_name  VARCHAR,
            phone      VARCHAR,
            banned     INTEGER,
            timeout    DATETIME
        );
         """)
    conn.commit()

def if_user_exists(chat_id):
    try:
        cursor.execute("SELECT * FROM users WHERE chat_id = ?", [chat_id])
        user_g = cursor.fetchall()
        log.debug(user_g[0][1] + " was checked on existing")
        return True
    except IndexError:
        return False

def if_user_ban(username):
    cursor.execute("SELECT banned FROM users WHERE username LIKE ?", [username])
    user_g = cursor.fetchall()
    return user_g[0][0]

def if_user_ban_2(chat_id):
    cursor.execute("SELECT banned FROM users WHERE chat_id = ?", [chat_id])
    user_g = cursor.fetchall()
    return user_g[0][0]

def banlist():
    cursor.execute("SELECT chat_id, username FROM users WHERE banned = 1",)
    result = cursor.fetchall()
    return result

def new_user(chat_id, username, first_name, last_name):
    cursor.execute("""INSERT INTO users (chat_id, username, first_name, last_name, phone, banned, timeout) VALUES (?, ?, ?, ?, ?, ?, ?)
""", (chat_id, username, first_name, last_name, 0, 0, 0))
    conn.commit()

def update_phone(chat_id, phone):
    cursor.executemany("""UPDATE users 
    SET phone = ? WHERE chat_id = ?""", ((phone, chat_id), ))
    conn.commit()

def update_ban(username):
    cursor.executemany("""UPDATE users 
    SET banned = 1 WHERE username LIKE ?""", ((username, ), ))
    conn.commit()

def update_unban(username):
    cursor.executemany("""UPDATE users 
    SET banned = 0 WHERE username = ?""", ((username, ), ))
    conn.commit()

def update_timeout_on(date, chat_id):
    cursor.executemany("""UPDATE users 
    SET timeout = ? WHERE chat_id = ?""", ((date, chat_id), ))
    conn.commit()

def get_timeout(chat_id):
    cursor.execute("SELECT timeout FROM users WHERE chat_id = ?", [chat_id])
    time_g = cursor.fetchall()
    return time_g[0][0]