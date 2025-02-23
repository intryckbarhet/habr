import sqlite3
import datetime

db ="data.db"
def createposttable():
    SQL ="""
    CREATE TABLE IF NOT EXISTS post (
        id INTEGER PRIMARY KEY,
        title  TEXT,
        text TEXT
        at_publish TEXT,
        author_id INTEGER
    )
    """
    con = sqlite3.connect(db)
    con.execute(SQL)

class Post:
    def __init__(self, id, title, text, at_publish, author_id):
        self.id = id
        self.title = title
        self.text = text
        self.at_publish = at_publish
        self.author_id = author_id

    @staticmethod
    def getallposts():
        SQL = """
         SELECT * FROM post
        """
        con = sqlite3.connect(db)
        q = con.execute(SQL)
        data = q.fetchall()

        return [Post(*row) for row in data]

    @staticmethod
    def getallpostsbyauthor(author_id):
        SQL = """
         SELECT * FROM post
         WHERE author_id = ?
        """
        con = sqlite3.connect(db)
        q = con.execute(SQL, [author_id])
        data = q.fetchall()

        return [Post(*row) for row in data]
    
    @staticmethod
    def create(title, text, author_id):
        SQL = """
            INSERT INTO post(title, text, at_publish, author_id)
            VALUES (?, ?, ?, ?)
        """
        con = sqlite3.connect(db)
        con.execute(SQL, [title, text, datetime.datetime.now().strftime("%d.%m.%Y %H:%M"), author_id])