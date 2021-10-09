import psycopg2


class WrongScheduleFormat(Exception):
    def __init__(self):
        self.message = ("Invalid schedule format. Expected format: "
                        "UTC<UTC time zone> <start> <end>. "
                        "Start and end are hour in 24 hours format")
        super().__init__(self.message)


class StartAfterEndError(Exception):
    def __init__(self):
        self.message = ("Looks like you are starting your "
                        "practice after you finish it")
        super().__init__(self.message)


class HoursOutOfRangeError(Exception):
    def __init__(self, hours):
        self.message = f"Hours out of the range: {hours}"
        super().__init__(self.message)


class Schedule:
    """
    This class represents user-defined schedule
    """
    def __init__(self, timezone: int, begin: int, end: int):
        """
        :param timezone: Users timezone
        :param begin: hour when user starts practice (in user local time)
        :param end: hour when user ends practice (in user local time)
        :raises:
            HoursOutOfRangeError: given begin or end lies out of [0, 24] interval
            ValueError: provided timezone is not a valid UTC timezone
            StartAfterEndError: begin is after the end of the practice
        """
        self.timezone = timezone
        if not 0 <= begin <= 24:
            raise HoursOutOfRangeError(begin)
        if not 0 <= end <= 24:
            raise HoursOutOfRangeError(end)
        if not self.__valid_timezone():
            raise ValueError(f"Invalid timezone: {self.timezone}")
        self.begin = begin - self.timezone
        self.end = end - self.timezone
        if self.begin >= self.end:
            raise StartAfterEndError

    @staticmethod
    def from_string(schedule: str):
        """
        Builds Schedule object from the string of following format:
            UTC<timezone> <begin> <end>
        Where:
            <timezone> - valid UTC timezone number
            <begin> - beginning hour
            <end> - ending hour

        :param schedule: string representing schedule
        :returns: Schedule corresponding to a given string
        :raises:
            WrongScheduleFormat: schedule format is violated
            ValueError: Given <begin> or <end> can not be converted to integer
        """
        if not schedule:
            raise WrongScheduleFormat
        if not schedule.startswith("UTC"):
            raise WrongScheduleFormat

        schedule.removeprefix("UTC")
        try:
            timezone, begin, end = schedule.split(" ", maxsplit=2)
        except Exception as e:
            raise WrongScheduleFormat from e
        timezone = timezone.removeprefix("UTC")
        try:
            timezone = int(timezone)
        except Exception as e:
            raise ValueError(f"Invalid timezone: {timezone}") from e

        def parse_hour(hour: str):
            try:
                hour = int(hour)
            except Exception as e:
                raise ValueError(f"Invalid time format: {hour}. Expected hours") from e
            return hour
        begin = parse_hour(begin)
        end = parse_hour(end)
        return Schedule(timezone, begin, end)

    def __valid_timezone(self) -> bool:
        """
        Checks if Schedule object stores valid timezone
        """
        return -12 <= self.timezone <= 14

    def __str__(self):
        """
        Represent schedule as a string
        """
        return (f"Starting at {self.begin + self.timezone}. "
                f"Finishing at {self.end + self.timezone}.")

    def update(self, user_id: int, cursor: psycopg2.extensions.cursor):
        """
        Save schedule to database
        :param user_id: Telegram UserID whose schedule is being updated
        :param cursor: PostgreSQL client used to save schedule
        """
        cursor.callproc('update_user_time', [user_id, self.timezone, self.begin, self.end, ])
