import sqlite3

db ="data.db"
def createusertable():
    SQL ="""
    CREATE TABLE IF NOT EXISTS user (
        id INTEGER PRIMARY KEY,
        username TEXT UNIQUE,
        password TEXT
    )
    """
    con = sqlite3.connect(db)
    con.execute(SQL)

class User:
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    @staticmethod
    def getbyusername(username):
        SQL = """
         SELECT * FROM user
         WHERE username = ?
        """
        con = sqlite3.connect(db)
        q = con.execute(SQL, [username])
        data = q.fetchone()
        if not data:
            return None
        return User(*data)
    
    @staticmethod
    def create(username, password):
        SQL = """
            INSERT INTO user(username, password)
            VALUES (?, ?)
        """
        con = sqlite3.connect(db)
        con.execute(SQL, [username, password])
        con.commit()