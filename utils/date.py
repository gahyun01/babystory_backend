from datetime import datetime
from typing import Union, Set


def process_str_date(start: str = None, end: str = None) -> Union[str, Set[datetime]]:
    start_date = None
    end_date = None

    if start == None and end == None:
        end_date = datetime.now()
        start_date = end_date.replace(day=end_date.day-7)

    if start != None and end == None:
        end_date = datetime.now()

    if start == None and end != None:
        return "start date not provided"

    if start_date == None:
        try:
            start_date = datetime.strptime(start, '%Y-%m-%d')
        except Exception as e:
            return "date format is not correct"
    if end_date == None:
        try:
            end_date = datetime.strptime(end, '%Y-%m-%d')
        except Exception as e:
            return "date format is not correct"

    return start_date, end_date