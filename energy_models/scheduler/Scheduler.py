import datetime
from typing import Callable, List


class Scheduler:
    def __init__(
        self,
        default: List[float],
        weekend: List[float] = None,
        holiday: List[float] = None,
        interpolate: bool = False,
        holiday_dates: List[datetime.date] = None,
    ):
        """
        Generalized hourly schedule engine.

        Args:
            default (List[float]): 24-hour values for weekdays.
            weekend (List[float], optional): 24-hour values for weekends.
            holiday (List[float], optional): 24-hour values for holidays.
            interpolate (bool): Whether to interpolate between hours.
            holiday_dates (List[datetime.date], optional): List of holiday dates.
        """
        self.default = default
        self.weekend = weekend if weekend else default
        self.holiday = holiday if holiday else default
        self.interpolate = interpolate
        self.holiday_dates = set(holiday_dates or [])

    def _select_schedule(self, dt: datetime.datetime) -> List[float]:
        if dt.date() in self.holiday_dates:
            return self.holiday
        elif dt.weekday() >= 5:
            return self.weekend
        else:
            return self.default

    def get_value(self, t: float) -> float:
        """
        Evaluate schedule value at time t.

        Args:
            t (float): Time in hours since midnight (e.g., 13.5 = 1:30 PM)

        Returns:
            float: Schedule value at time t.
        """
        hours = int(t) % 24
        minutes = (t % 1.0) * 60
        dt = datetime.datetime.combine(
            datetime.date.today(), datetime.time(hour=hours, minute=int(minutes))
        )
        schedule = self._select_schedule(dt)

        if not self.interpolate:
            return schedule[dt.hour]

        h = dt.hour
        h_next = (h + 1) % 24
        fraction = dt.minute / 60.0
        return (1 - fraction) * schedule[h] + fraction * schedule[h_next]


# Factory functions to plug into the ZoneExhaustFan class


def make_flow_fraction_schedule(schedule: Schedule) -> Callable[[float], float]:
    return lambda t: schedule.get_value(t)


def make_availability_schedule(
    schedule: Schedule, threshold: float = 0.1
) -> Callable[[float], bool]:
    return lambda t: schedule.get_value(t) > threshold
