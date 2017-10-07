import os, json
from config import DST_FOLDER
from helpers import itermedia, is_photo, tmp_dir, parse_date, external, ensure_dir


def lowres_photos(tmp_dir):
    photo_map = {}
    for photo_path, media_name in itermedia():
        photo_name = os.path.splitext(media_name)[0] + '.jpg'
        year, month, day = parse_date(photo_name)
        if year is None:
            print "Unkown format", photo_name
            continue
        dst_dir = os.path.join(DST_FOLDER, year, month)
        dst_file = os.path.join(dst_dir, photo_name)

        thumb_dir = os.path.join(dst_dir, 'thumbs')
        thumb_file = os.path.join(thumb_dir, photo_name)
        ensure_dir(thumb_dir)

        photo_map[photo_path] = dst_file

        if not os.path.exists(dst_file):
            if is_photo(media_name):
                external('convert', photo_path, '-resize', '800x600>', '-auto-orient', '-quality', '65', '-strip', dst_file)
            else:
                tmp_name = os.path.join(tmp_dir, photo_name)
                external('ffmpeg', '-i', photo_path, '-vframes', '1', tmp_name)
                external('convert', tmp_name, '-resize', '800x600>', '-auto-orient', '-quality', '65', '-strip', dst_file)

        if not os.path.exists(thumb_file):
            external('convert', dst_file, '-resize', '200x175>', '-quality', '65', '-strip', thumb_file)

    with open(os.path.join(DST_FOLDER, 'index.json'), 'w') as f:
        f.write(json.dumps(photo_map))


if __name__ == '__main__':
    with tmp_dir() as tmp:
        lowres_photos(tmp)
