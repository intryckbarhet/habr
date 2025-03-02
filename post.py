import sqlite3
import datetime

db ="data.db"
def createposttable():
    con = sqlite3.connect(db)
    SQL = """
    CREATE TABLE IF NOT EXISTS post (
        id INTEGER PRIMARY KEY,
        title TEXT,
        text TEXT,
        at_publish TEXT,
        author_id INTEGER,
        image_url TEXT
    )"""
    
    con.execute(SQL)
    SQL = """
    CREATE TABLE IF NOT EXISTS likes (
        id INTEGER PRIMARY KEY,
        user_id INTEGER,
        post_id INTEGER,
        UNIQUE(user_id, post_id)
    );
    """
    con.execute(SQL)
    

class Post:
    def __init__(self, id, title, text, at_publish, author_id, username=None):
        self.id = id
        self.title = title
        self.text = text
        self.at_publish = at_publish
        self.author_id = author_id
        self.author_un = username

    @staticmethod
    def getallposts():
        SQL = """
         SELECT post.*, user.username FROM post
         LEFT JOIN user ON user.id = post.author_id
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
        con.commit()

    @staticmethod
    @staticmethod
    def togglelike(user_id, post_id):
        SQL_check = "SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?"
        con = sqlite3.connect(db)
        cursor = con.cursor()
        cursor.execute(SQL_check, [user_id, post_id])
        exists = cursor.fetchone()

        if exists:
            SQL_delete = "DELETE FROM likes WHERE user_id = ? AND post_id = ?"
            con.execute(SQL_delete, [user_id, post_id])
            con.commit()
            return False
        else:
            SQL_insert = "INSERT INTO likes (user_id, post_id) VALUES (?, ?)"
            con.execute(SQL_insert, [user_id, post_id])
            con.commit()
            return True  # Лайк добавлен


    @staticmethod
    def getlikescount(post_id):
        SQL = "SELECT COUNT(*) FROM likes WHERE post_id = ?"
        con = sqlite3.connect(db)
        q = con.execute(SQL, [post_id])
        return q.fetchone()[0]

    @staticmethod
    def is_liked_by_user(user_id, post_id):
        SQL = "SELECT 1 FROM likes WHERE user_id = ? AND post_id = ?"
        con = sqlite3.connect(db)
        q = con.execute(SQL, [user_id, post_id])
        return q.fetchone() is not None
