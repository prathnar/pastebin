import sqlite3
import uuid

conn = sqlite3.connect("pastes.db", check_same_thread=False)


cursor = conn.cursor()

# cursor.execute("DROP TABLE pastes")

cursor.execute("""CREATE TABLE IF NOT EXISTS pastes
               (
               paste_id STRING PRIMARY KEY,
               title TEXT NOT NULL,
               content TEXT NOT NULL,
               expiry STRING NOT NULL,
               is_password_protected STRING NOT NULL DEFAULT 0,
               password STRING,
               language STRING,
               burn_after_read SRING NOT NULL 
               )""")

def add_entry(uid, title, content, expiry, is_password, password, language, burn_after_read):
    
    cursor.execute(f"""
                   INSERT INTO pastes (paste_id, title, content, expiry, is_password_protected, password, language, burn_after_read) VALUES
                    (?, ?, ?, ?, ?, ?, ?, ?)
                   """,
                   (uid,title, content, expiry, is_password, password, language, burn_after_read))
 
    conn.commit()

def get_data(id):
    cursor.execute(f"SELECT * FROM pastes WHERE paste_id = '{id}'")

    results = cursor.fetchall()

    return results

def delete_entry(uid):
    cursor.execute(f"DELETE FROM pastes WHERE paste_id = '{uid}'")
    print('inside db')
    conn.commit()
 
conn.commit()

# conn.close()






