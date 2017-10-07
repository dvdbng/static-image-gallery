import os, itertools, json, re
DST_FOLDER = '/home/owncloud/bengoa/files/photos/'

with open(os.path.join(DST_FOLDER, 'index.json'), 'r') as f:
    photo_map = json.loads(f.read())


print """

check() {
    if identify -format "%[EXIF:*]" "$1" | grep -v 'Orientation=1' | grep Orientation
    then
        echo rm "'$2'" "'$3'" "'$4'"
    fi
}
"""


for orig, small in photo_map.iteritems():
    thumb = os.path.join(os.path.dirname(small), 'thumbs', os.path.basename(small))
    json = os.path.splitext(small)[0] + '.json'
    print "check '%s' '%s' '%s' '%s'" % (orig, small, thumb, json)

