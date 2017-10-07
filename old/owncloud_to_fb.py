import os
import re
import fbconsole

# Get from https://developers.facebook.com/tools/explorer
fbconsole.ACCESS_TOKEN = ''  # NOQA

ORIGIN_FOLDERS = (
    '/home/owncloud/bengoa/files/InstantUpload',
)

START = '2016', '05', '14'
END = '2016', '06', '14'
ALBUM = "10205803054110528"


def is_photo(path):
    name, ext = os.path.splitext(path)
    return ext in (".png", ".jpg")


def parse_date(name):
    m = re.match('(201N)(NN)(NN)'.replace('N', '\\d'), name)
    if m:
        return m.group(1), m.group(2), m.group(3)
    return None, None, None


def iterphotos():
    for folder in ORIGIN_FOLDERS:
        for dir_name, subdirs, files in os.walk(folder):
            for file_name in files:
                if is_photo(file_name):
                    yield os.path.join(folder, dir_name, file_name), file_name


for photo_path, photo_name in iterphotos():
    date = parse_date(photo_name)
    if date[0] is None:
        print "Unkown format", photo_name
        continue
    if date < START and date >= END:
        continue

    with open(photo_path, 'rb') as f:
        fbconsole.post('/%s/photos' % ALBUM, {"source": f})
