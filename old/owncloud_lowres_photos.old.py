import os, re, subprocess

ORIGIN_FOLDERS = (
    '/home/owncloud/bengoa/files/InstantUpload',
)

DST_FOLDER = '/home/owncloud/bengoa/files/photos/'


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
    year, month, day = parse_date(photo_name)
    if year is None:
        print "Unkown format", photo_name
        continue
    dst_dir = os.path.join(DST_FOLDER, year, month)
    dst_file = os.path.join(dst_dir, photo_name)

    if os.path.exists(dst_file):
        continue

    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    subprocess.call(['convert', photo_path, '-resize', '800x600>', '-quality', '65', '-strip', dst_file])

