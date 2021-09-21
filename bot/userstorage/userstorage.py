import psycopg2
import logging
from bot.userstorage.missingdatabaseurlerror import MissingUserDatabaseURLError
from bot.Schedule import Schedule


class UserStorage:
    def __init__(self, db_url):
        if not db_url:
            raise MissingUserDatabaseURLError
        self.conn = psycopg2.connect(db_url)
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

    def create_user(self, user_id: int):
        self.cursor.callproc('create_user', [user_id, 1, "active", 0, 10, 18,])
        status = self.cursor.fetchone()

    def user_exists(self, user_id: int):
        self.cursor.callproc('user_exists', [user_id])
        result = self.cursor.fetchone()[0]
        logging.debug(f"user_exists({user_id}) = {result}")
        return result

    def update_user_schedule(self, user_id: int, schedule: Schedule):
        if self.user_exists(user_id):
            schedule.update(user_id, self.cursor)
        else:
            raise UpdaitingNonExistingUserError

    def __del__(self):
        self.cursor.close()
        self.conn.close()
