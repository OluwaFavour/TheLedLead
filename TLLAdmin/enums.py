# Define Month Enum
import enum


class Month(enum.Enum):
    JANUARY = 1
    FEBRUARY = 2
    MARCH = 3
    APRIL = 4
    MAY = 5
    JUNE = 6
    JULY = 7
    AUGUST = 8
    SEPTEMBER = 9
    OCTOBER = 10
    NOVEMBER = 11
    DECEMBER = 12


"""
    Get the month name from the month number
    :param month: The month number

    Returns:
        str: The month name or None if the month number is invalid
"""
def getMonth(month: int):
    try:
        return Month(month).name
    except ValueError:
        return None