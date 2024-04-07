from dataclasses import dataclass

from datetime import datetime, UTC
import calendar


@dataclass
class VagueDate:
    year: int
    month: int = None
    day: int | float = None
    hour: int = None
    minute: int = None
    second: int | float = None
    uncertain: bool = False
    scheduled: bool = False
    string: str = None

    def __str__(self):
        return self.string

    @property
    def month_str(self) -> str:
        return calendar.month_abbr[self.month]

    def _add_info(self, info: str) -> str:
        if self.uncertain:
            info += '?'
        if self.scheduled:
            info += 's'
        return info

    @classmethod
    def from_string(cls, date: str):
        return cls(*cls._parse_datetime(date), string=date)

    @classmethod
    def _parse_datetime(cls, date: str) -> tuple:
        uncertain = False
        scheduled = False
        if '?' in date:
            date = date.replace('?', '')
            uncertain = True
        if 's' in date:
            date = date.replace('s', '')
            scheduled = True
        date = date.strip()
        split_date = date.split(' ')
        year = int(split_date[0])
        month = None
        day = None
        hour = None
        minute = None
        second = None
        if len(split_date) > 1:
            month = cls._parse_month(split_date[1])
        if len(split_date) > 2:
            day, hour, minute, second = cls._parse_day(split_date[2])
        if len(split_date) > 3 and hour is None and minute is None and second is None:
            hour, minute, second = cls._parse_time(split_date[3])

        return year, month, day, hour, minute, second, uncertain, scheduled

    @staticmethod
    def _parse_month(month):
        if month.isdigit():
            return int(month)
        return list(calendar.month_abbr).index(month)

    @staticmethod
    def _parse_day(day):
        if '.' in day:
            day_int = int(day.split('.')[0])
            day_float = float(day) - day_int
            # transform the fraction of the day into hours and minutes and seconds
            day_float = day_float * 24
            hour = int(day_float)
            day_float = (day_float - hour) * 60
            minute = int(day_float)
            day_float = (day_float - minute) * 60
            second = int(day_float)
            return day_int, hour, minute, second
        return int(day), None, None, None

    @staticmethod
    def _parse_time(time):
        if 'h' in time:
            time = time.replace('h', '')
            return int(time), None, None
        else:
            hours = int(time[:2])
            minutes = int(time[2:4])
            seconds = None
            if len(time) > 4:
                if '.' in time:
                    seconds = float(time[5:])
                else:
                    seconds = int(time[5:])
            return hours, minutes, seconds

    @property
    def datetime(self):
        if self.month is None:
            return datetime(self.year, 1, 1, tzinfo=UTC)
        if self.day is None:
            return datetime(self.year, self.month, 1, tzinfo=UTC)
        if self.hour is None:
            return datetime(self.year, self.month, self.day, tzinfo=UTC)
        if self.minute is None:
            return datetime(self.year, self.month, self.day, self.hour, 0, tzinfo=UTC)
        if self.second is None:
            return datetime(self.year, self.month, self.day, self.hour, self.minute, tzinfo=UTC)
        if isinstance(self.second, float):
            return datetime(self.year, self.month, self.day, self.hour, self.minute, int(self.second),
                            int((self.second - int(self.second)) * 1e6), tzinfo=UTC)
        return datetime(self.year, self.month, self.day, self.hour, self.minute, self.second, tzinfo=UTC)


if __name__ == '__main__':
    vague_dates = [
        "2016 Jun 8 2355:57.345",
        "2016 Jun 8 2355:57",
        "2016 Jun 8 2355:57?",
        "2016 Jun 8 2355",
        "2016 Jun 8 2355?",
        "2016 Jun 8.98",
        "2016 Jun 8.98?",
        "2016 Jun 8 23h",
        "2016 Jun 8.9",
        "2016 Jun 8",
        "2016 Jun 8s",
        "2016 Jun 8?",
        "2016 Jun",
        "2016 Jun?",
        "2016"
    ]

    for d in vague_dates:
        vague_date = VagueDate.from_string(d)
        print(vague_date)
        print(vague_date.datetime)
        print()
