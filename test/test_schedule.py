from bot.Schedule import HoursOutOfRangeError, Schedule, StartAfterEndError, WrongScheduleFormat
import pytest

class TestSchedule:
    def test_requires_UTC_prefix(self):
        with pytest.raises(WrongScheduleFormat):
            schedule = "+3 13 25"
            schedule = Schedule(schedule)

    def test_limits_hours_start(self):
        with pytest.raises(HoursOutOfRangeError):
            schedule = "UTC+3 -7 12"
            schedule = Schedule(schedule)

    def test_limits_hours_end(self):
        with pytest.raises(HoursOutOfRangeError):
            schedule = "UTC+7 7 234"
            schedule = Schedule(schedule)

    def test_panics_if_start_is_after_the_end(self):
        with pytest.raises(StartAfterEndError):
            schedule = "UTC-12 7 5"
            schedule = Schedule(schedule)

    def test_panics_on_wrong_timezone(self):
        with pytest.raises(ValueError, match = "Invalid timezone*"):
            schedule = "UTC-13 7 15"
            schedule = Schedule(schedule)
