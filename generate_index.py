import os, itertools, json, re
from contextlib import contextmanager

from helpers import parse_date
from shared import get_shared
from config import DST_FOLDER

VERSION = 14

with open(os.path.join(DST_FOLDER, 'index.json'), 'r') as f:
    photo_map = json.loads(f.read())


@contextmanager
def gen_file(fn):
    directory = os.path.dirname(fn)
    def path(fn): # fn either absolute or DST_FOLDER-relative
        return os.path.relpath(os.path.join(DST_FOLDER, fn), directory)
    if not os.path.exists(directory):
        os.makedirs(directory)
    with open(fn, 'w') as f:
        f.write('<!DOCTYPE html><html><head><meta http-equiv="content-type" content="text/html; charset=utf-8">')
        for style in (
                'style.css',
                'node_modules/@fancyapps/fancybox/dist/jquery.fancybox.min.css',
            ):
            f.write('<link rel="stylesheet" href="%s"/>' % path('assets/%s?v=%s' % (style, VERSION)))
        f.write("<body>")

        yield (f, path)

        for script in (
          'node_modules/jquery/dist/jquery.min.js',
          'node_modules/jquery-unveil/jquery.unveil.js',
          'node_modules/@fancyapps/fancybox/dist/jquery.fancybox.min.js',
          'main.js'):
            f.write('<script src="%s" type="text/javascript"></script>' % path('assets/%s?v=%s' % (script, VERSION)))

        f.write("</body></html>")


def gen_index(fn, photos):
    with gen_file(fn) as (f, path):
        for orig, small in photos:
            thumb = os.path.join(os.path.dirname(small), 'thumbs', os.path.basename(small))
            f.write('\n<a href="%s" target="_blank" data-full-size="%s">%s</a>' % (path(small), path(orig), image(small, path(thumb))))


def gen_index_list(fn, indexes): # indexes = [name, path, [[small, orig]]...]...
    with gen_file(fn) as (f, path):
        for (name, index_path, images) in indexes:
            f.write('<a href="%s">%s (%s)</a><br/>\n' % (path(index_path), name, len(images)))
            for orig, small in images[:5]:
                thumb = os.path.join(os.path.dirname(small), 'thumbs', os.path.basename(small))
                f.write(image(small, path(thumb)))
            f.write('<hr/>')

def image(name, path):
    alt = category_by_image.get(name, '')
    return '\n<img data-src="%s" title="%s" src="//:0"/>' % (path, alt)




# Read category data
images_by_category = {} # category -> [[orig, small, score]...]
category_by_image = {} # image -> [[category, score]... ]
for orig, small in photo_map.iteritems():
    meta_path = os.path.splitext(small)[0] + '.json'
    if not os.path.exists(meta_path):
        continue
    with open(meta_path) as f:
        categories = json.loads(f.read())['contents']

    imgcategories = []
    for category, score in categories.iteritems():
        if score < 0.1:
            continue
        images_by_category.setdefault(category, []).append([orig, small, score])
        imgcategories.append([category, score])

    imgcategories.sort(key=lambda item: -item[1])
    category_by_image[small] = "Image might contain: " + (", ".join(item[0] for item in imgcategories))



# Indexes by date
keyfn = lambda item: os.path.dirname(item[1])
filekeyfn = lambda item: os.path.basename(item[1])[:8]
items = sorted(photo_map.iteritems(), key=keyfn)
by_month = [(dir, list(photos)) for dir, photos in itertools.groupby(items, keyfn)]


gen_index_list(os.path.join(DST_FOLDER, 'by_month.html'), [
    [month, os.path.join(month, 'index.html'), photos]
    for month, photos in by_month
])

for dir, photos in by_month:
    photos = sorted(list(photos), key=lambda item: os.path.basename(item[1]))
    print dir, len(photos)
    gen_index(os.path.join(dir, 'index.html'), photos)

    # Split by day
    by_day = [(day, list(dayphotos)) for day, dayphotos in itertools.groupby(photos, key=lambda item: parse_date(os.path.basename(item[1]))[2])]
    gen_index_list(os.path.join(dir, 'days.html'), [
        [day, os.path.join(dir, '%s.html' % day), dayphotos]
        for day, dayphotos in by_day
    ])
    for day, dayphotos in by_day:
        gen_index(os.path.join(dir, '%s.html' % day), list(dayphotos))

# Shared photos
for shared_key, photos in get_shared(photo_map):
    photos = sorted(list(photos), key=lambda item: parse_date(os.path.basename(item[1])), reverse=True)
    gen_index(os.path.join(DST_FOLDER, 'shared', shared_key, 'index.html'), photos)
    print(shared_key, len(photos))

# Indexes by category
for category, images in images_by_category.iteritems():
    images.sort(key=lambda i: -i[2])
    name = re.sub('[^a-zA-Z]+', '_', category) + '.html'
    gen_index(os.path.join(DST_FOLDER, 'categories', name), [(orig, small) for orig, small, score in images])


sorted_categories = sorted(images_by_category.items(), key=lambda x: -sum([score for (o, s, score) in x[1]]))
gen_index_list(
    os.path.join(DST_FOLDER, 'categories.html'),
    [
        [
            category,
            os.path.join(DST_FOLDER, 'categories', re.sub('[^a-zA-Z]+', '_', category) + '.html'),
            [(orig, small) for orig, small, score in images]
        ]
        for category, images in sorted_categories
    ]
)

