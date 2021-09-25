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


# Works with schedule in format
# UTC<UTC time zone> <start> <end>
class Schedule:
    def __init__(self, schedule: str):
        if not schedule:
            raise WrongScheduleFormat
        if not schedule.startswith("UTC"):
            raise WrongScheduleFormat

        schedule.removeprefix("UTC")
        try:
            timezone, begin, end = schedule.split(" ", maxsplit=2)
        except Exception:
            raise WrongScheduleFormat
        timezone = timezone.removeprefix("UTC")
        self.__parse_timezone(timezone)
        self.begin = self.__parse_hour(begin) - self.timezone
        self.end = self.__parse_hour(end) - self.timezone
        if self.begin >= self.end:
            raise StartAfterEndError

    def __parse_timezone(self, timezone):
        try:
            self.timezone = int(timezone)
        except Exception:
            raise ValueError(f"Invalid timezone: {timezone}")
        if not -12 <= self.timezone <= 14:
            raise ValueError(f"Invalid timezone: {self.timezone}. "
                             "According to UTC standard, timezones start from "
                             "UTC-12 and end at UTC+14")

    def __parse_hour(self, hour):
        try:
            hour = int(hour)
        except Exception:
            raise ValueError(f"Invalid time format: {hour}. Expected hours")
        if not 0 <= hour <= 24:
            raise HoursOutOfRangeError(hour)
        return hour

    def __str__(self):
        return (f"Starting at {self.begin + self.timezone}. "
                f"Finishing at {self.end + self.timezone}.")

    def update(self, user_id, cursor: psycopg2.extensions.cursor):
        cursor.callproc('update_user_time', [user_id, self.timezone, self.begin, self.end,])
