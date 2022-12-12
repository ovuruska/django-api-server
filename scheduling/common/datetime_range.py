from datetime import datetime, timedelta
from typing import Generator


def datetime_range(start: datetime, end: datetime, delta: timedelta) -> Generator[datetime, None, None]:
    while start <= end:
        yield start
        start += delta