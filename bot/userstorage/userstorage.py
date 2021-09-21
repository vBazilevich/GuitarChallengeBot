import logging
import psycopg2
from bot.userstorage import MissingUserDatabaseURLError
from bot.userstorage import UpdatingNonExistingUserError
from bot.Schedule import Schedule


class UserStorage:
    def __init__(self, db_url):
        if not db_url:
            raise MissingUserDatabaseURLError
        self.conn = psycopg2.connect(db_url)
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

    def test_create_user(self, user_id: int):
        self.cursor.callproc('create_user', [user_id, 1, "active", 0, 10, 18,])
        self.cursor.fetchone()

    def user_exists(self, user_id: int):
        self.cursor.callproc('user_exists', [user_id])
        result = self.cursor.fetchone()[0]
        logging.debug(f"user_exists({user_id}) = {result}")
        return result

    def update_user_schedule(self, user_id: int, schedule: Schedule):
        if self.user_exists(user_id):
            schedule.update(user_id, self.cursor)
        else:
            raise UpdatingNonExistingUserError(user_id)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        self.conn.close()
