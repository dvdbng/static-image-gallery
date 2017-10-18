import re
import os
import subprocess
import tempfile
from contextlib import contextmanager

from config import ORIGIN_FOLDERS, TEST

PHOTO_EXT = ('png', 'jpg')
MEDIA_EXT = PHOTO_EXT + ('mp4',)
PHOTO_RE = re.compile('\.%s$' % '|'.join(PHOTO_EXT), re.I)
MEDIA_RE = re.compile('\.%s$' % '|'.join(MEDIA_EXT), re.I)

def is_photo(path):
    return PHOTO_RE.search(path) is not None

def is_media(path):
    return MEDIA_RE.search(path) is not None

FILE_REGEXPS = [
    re.compile(
        source.replace('YYYY', '(?P<y>20\d\d)')
       .replace('MM'  , '(?P<m>\d\d)')
       .replace('DD'  , '(?P<d>\d\d)')
       .replace('hh'  , '(?P<h>\d\d)')
       .replace('mm'  , '(?P<min>\d\d)')
       .replace('ss'  , '(?P<s>\d\d)')
    ) for source in
    'YYYYMMDDhhmmss',
    'IMG_YYYYMMDD_hhmmss',
    'FB_IMG_YYYYMMDDhhmmss',
    'MM-DD-YYYY-hh-mm-ss',
    'YYYYMMDD',
    'IMG_YYYYMMDD',
    'FB_IMG_YYYYMMDD',
    'MM-DD-YYYY-',
]

def parse_date_time(name):
    for rx in FILE_REGEXPS:
        m = rx.match(name)
        if m:
            g = m.groupdict()
            return g['y'], g['m'], g['d'], g.get('h', 0), g.get('min', 0), g.get('s', 0)
    return None, None, None, None, None, None


def parse_date(name):
    return parse_date_time(name)[:3]

def itermedia():
    for folder in ORIGIN_FOLDERS:
        for dir_name, subdirs, files in os.walk(folder):
            for file_name in files:
                if is_media(file_name):
                    yield os.path.join(folder, dir_name, file_name), file_name

def iterphotos():
    for path, name in itermedia():
        if is_photo(name):
            yield path, name

def external(*args):
    if TEST:
        print args
    return subprocess.call(args)

def ensure_dir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)

@contextmanager
def tmp_dir():
    dir = tempfile.mkdtemp()
    try:
        yield dir
    finally:
        external('rm', '-rf', dir)

