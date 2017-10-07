import hashlib
import os

from helpers import parse_date
from config import SHARED

def excluded(date, time):
    return False

def get_shared(photos):
    by_shared = [[key, []] for key in SHARED.keys()]
    for item in photos.iteritems():
        for key, list in by_shared:
            date = parse_date(os.path.basename(item[0]))
            time = None # TODO
            if date:
                date = tuple(map(int, date))
                if SHARED[key](date, time) and not excluded(date, time):
                    list.append(item)

    return by_shared

