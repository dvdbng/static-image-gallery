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
    ) for source in
    'YYYYMMDD',
    'IMG_YYYYMMDD',
    'FB_IMG_YYYYMMDD',
    'MM-DD-YYYY-',
]

def parse_date(name):
    for rx in FILE_REGEXPS:
        m = rx.match(name)
        if m:
            return m.group('y'), m.group('m'), m.group('d')
    return None, None, None

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

