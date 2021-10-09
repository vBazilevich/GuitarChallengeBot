import logging
import psycopg2
from bot.userstorage import MissingUserDatabaseURLError
from bot.userstorage import UpdatingNonExistingUserError
from bot.userstorage.accessingnonexistingusererror import AccessingNonExistingUserError
from bot.schedule import Schedule


class UserStorage:
    """
    This class implements interaction with database that
    stores information about users.

    Uses PostgreSQL database. Check SQL folder for database
    scheme as well as provided procedures.
    """
    def __init__(self, db_url):
        """
        :param db_url: URL of database server with cridentials required
                       to establish the connection
        :raises:
            MissingUserDatabaseURLError: no database URL was provided
        """
        self.conn = None
        self.cursor = None
        if not db_url:
            raise MissingUserDatabaseURLError
        self.conn = psycopg2.connect(db_url)
        self.conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        self.cursor = self.conn.cursor()

    def create_user(self, user_id: int):
        """
        Creates a new user with given ID and default values for status,
        level and schedule
        :param user_id: Telegram UserID
        """
        self.cursor.callproc('create_user', [user_id, 1, "active", 0, 10, 18, ])
        self.cursor.fetchone()

    def user_exists(self, user_id: int) -> bool:
        """
        Check if there is a user with specified ID in database
        :param user_id: Telegram UserID
        """
        self.cursor.callproc('user_exists', [user_id])
        result = self.cursor.fetchone()[0]
        logging.debug(f"user_exists({user_id}) = {result}")
        return result

    def update_user_schedule(self, user_id: int, schedule: Schedule):
        """
        Used to set a new schedule for the user
        :param user_id: Telegram UserID
        :param schedule: new schedule of the user
        :raises:
            UpdatingNonExistingUserError: no user with given ID
        """
        if self.user_exists(user_id):
            schedule.update(user_id, self.cursor)
        else:
            raise UpdatingNonExistingUserError(user_id)

    def get_user_schedule(self, user_id: int) -> Schedule:
        """
        :param user_id: Telegram UserID
        :returns: schedule that user has registered or default one that was
                  created while registering user
        :raises:
            AccessingNonExistingUserError: no user with given id
        """
        if self.user_exists(user_id):
            self.cursor.callproc('fetch_user_time', [user_id])
            schedule = self.cursor.fetchone()
            timezone, begin, end = schedule
            result = Schedule(timezone, begin, end)
            return result
        raise AccessingNonExistingUserError(user_id)

    def get_user_level(self, user_id: int) -> int:
        """
        :param user_id: Telegram UserID
        :returns: the last level user has passed
        :raises:
            AccessingNonExistingUserError: no user with given id
        """
        if self.user_exists(user_id):
            self.cursor.callproc('fetch_user_level', [user_id])
            return self.cursor.fetchone()
        raise AccessingNonExistingUserError(user_id)

    def update_user_level(self, user_id: int):
        """
        Increments user level
        :param user_id: Telegram UserID
        :raises:
            UpdatingNonExistingUserError: no user with given ID
        """
        if self.user_exists(user_id):
            self.cursor.callproc('update_user_level', [user_id])
            self.cursor.fetchone()
        else:
            raise UpdatingNonExistingUserError(user_id)

    def reset_user_progress(self, user_id: int):
        """
        Returns user to level 1
        :param user_id: Telegram UserID
        :raises:
            UpdatingNonExistingUserError: no user with given ID
        """
        if self.user_exists(user_id):
            self.cursor.callproc('reset_user_progress', [user_id])
            self.cursor.fetchone()
        else:
            raise UpdatingNonExistingUserError(user_id)

    def __del__(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
