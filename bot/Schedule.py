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
    def __init__(self, timezone: int, begin: int, end: int):
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
        try:
            timezone = int(timezone)
        except Exception:
            raise ValueError(f"Invalid timezone: {timezone}")

        def parse_hour(hour: str):
            try:
                hour = int(hour)
            except Exception:
                raise ValueError(f"Invalid time format: {hour}. Expected hours")
            return hour
        begin = parse_hour(begin)
        end = parse_hour(end)
        return Schedule(timezone, begin, end)

    def __valid_timezone(self) -> bool:
        return -12 <= self.timezone <= 14

    def __str__(self):
        return (f"Starting at {self.begin + self.timezone}. "
                f"Finishing at {self.end + self.timezone}.")

    def update(self, user_id, cursor: psycopg2.extensions.cursor):
        cursor.callproc('update_user_time', [user_id, self.timezone, self.begin, self.end, ])
