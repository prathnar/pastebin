# import sqlite3
# import uuid

# conn = sqlite3.connect("pastes.db", check_same_thread=False)


# cursor = conn.cursor()

# # cursor.execute("DROP TABLE pastes")

# cursor.execute("""CREATE TABLE IF NOT EXISTS pastes
#                (
#                paste_id STRING PRIMARY KEY,
#                title TEXT NOT NULL,
#                content TEXT NOT NULL,
#                expiry STRING NOT NULL,
#                is_password_protected STRING NOT NULL DEFAULT 0,
#                password STRING,
#                language STRING,
#                burn_after_read SRING NOT NULL 
#                )""")

# def add_entry(uid, title, content, expiry, is_password, password, language, burn_after_read):
    
#     cursor.execute(f"""
#                    INSERT INTO pastes (paste_id, title, content, expiry, is_password_protected, password, language, burn_after_read) VALUES
#                     (?, ?, ?, ?, ?, ?, ?, ?)
#                    """,
#                    (uid,title, content, expiry, is_password, password, language, burn_after_read))
 
#     conn.commit()

# def get_data(id):
#     cursor.execute(f"SELECT * FROM pastes WHERE paste_id = '{id}'")

#     results = cursor.fetchall()

#     return results

# def delete_entry(uid):
#     cursor.execute(f"DELETE FROM pastes WHERE paste_id = '{uid}'")
#     print('inside db')
#     conn.commit()
 
# conn.commit()

# # conn.close()






import os
import uuid
from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, String, Text, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker

# Load environment variables
load_dotenv()

# Example: your .env should contain
# DATABASE_URL=postgresql+psycopg2://user:password@db_host:5432/db_name

USER = os.getenv('user')
PASSWORD = os.getenv('password')
HOST = os.getenv('host')
PORT = os.getenv('port')
DBNAME = os.getenv('dbname')

DATABASE_URL = f"postgresql+psycopg2://{USER}:{PASSWORD}@{HOST}:{PORT}/{DBNAME}?sslmode=require"

# Initialize SQLAlchemy
engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define the table model
class Paste(Base):
    __tablename__ = "pastes"

    paste_id = Column(String, primary_key=True, index=True)
    title = Column(Text, nullable=False)
    content = Column(Text, nullable=False)
    expiry = Column(String, nullable=False)
    is_password_protected = Column(Boolean, nullable=False, default=False)
    password = Column(String, nullable=True)
    language = Column(String, nullable=True)
    burn_after_read = Column(Boolean, nullable=False, default=False)

# Create tables (only the first time)
Base.metadata.create_all(bind=engine)

# Add entry
def add_entry(uid, title, content, expiry, is_password, password, language, burn_after_read):
    session = SessionLocal()
    try:
        new_paste = Paste(
            paste_id=uid,
            title=title,
            content=content,
            expiry=expiry,
            is_password_protected=bool(int(is_password)) if isinstance(is_password, str) else bool(is_password),
            password=password,
            language=language,
            burn_after_read=bool(int(burn_after_read)) if isinstance(burn_after_read, str) else bool(burn_after_read),
        )
        session.add(new_paste)
        session.commit()
    except Exception as e:
        session.rollback()
        print(f"Error adding entry: {e}")
    finally:
        session.close()

# Get data by ID
def get_data(paste_id):
    session = SessionLocal()
    try:
        result = session.query(Paste).filter(Paste.paste_id == paste_id).first()
        return result
    finally:
        session.close()

# Delete entry
def delete_entry(uid):
    session = SessionLocal()
    try:
        entry = session.query(Paste).filter(Paste.paste_id == uid).first()
        if entry:
            session.delete(entry)
            session.commit()
            print("Entry deleted from database.")
        else:
            print("No entry found with that ID.")
    except Exception as e:
        session.rollback()
        print(f"Error deleting entry: {e}")
    finally:
        session.close()
