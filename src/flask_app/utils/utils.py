import datetime

class Utils:

    @staticmethod
    def get_year_start_end(year: int) -> tuple[datetime.date, datetime.date]:
        start = datetime.date(year, 1, 1)
        end = datetime.date(year, 12, 31)
        return start, end