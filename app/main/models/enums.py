"""
All enums used in the schema are described here.
"""
import enum


class Reaction(enum.Enum):
    upvote = 1
    downvote = -1


class Month(enum.Enum):
    jan = 0
    feb = 1
    mar = 2
    apr = 3
    may = 4
    jun = 5
    jul = 6
    aug = 7
    sep = 8
    oct = 9
    nov = 10
    dec = 11
