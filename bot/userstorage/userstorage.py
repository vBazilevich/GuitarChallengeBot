import psycopg2
from bot.userstorage.missingdatabaseurlerror import MissingUserDatabaseURLError


class UserStorage:
    def __init__(self, db_url):
        if not db_url:
            raise MissingUserDatabaseURLError
        self.conn = psycopg2.connect(db_url)
        self.cursor = self.conn.cursor()

    def create_user(self, user_id: int):
        self.cursor.callproc('create_user', [user_id, 1, True, None, None, None])
        self.conn.commit()

    def user_exists(self, user_id: int):
        self.cursor.callproc('user_exists', [user_id])
        return self.cursor.fetchone()
