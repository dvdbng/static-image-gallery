from datetime import date
import os
today = date.today()

DST_FOLDER = '/home/owncloud/bengoa/files/photos/'

SHARED = {
    'ni': lambda d, t: d[:3] > (2016, 05, 15),
    'ni-iris-astrid': lambda d, t: d in ((2017, 9, 30), (2017, 10, 1)),
    'padres': lambda d, t: (
        d > (2015, 04, 13) and
        date(*d) < (date(2015, 06, 01) + (today.replace(day=1) - date(2017, 8, 1))*2)
    )
}

ORIGIN_FOLDERS = (
    '/home/owncloud/bengoa/files/InstantUpload',
    '/home/owncloud/bengoa/files/photos-etc',
    '/home/owncloud/bengoa/files/phone-etc',
    '/home/owncloud/bengoa/files/photos-s7',
    #'/home/david/Pictures/screenshots',
    #'s3://bengoa-img'
)

TEST = False

if os.environ.get('TEST'):
    TEST = True
    DST_FOLDER = '/home/david/dev/backup/test-out'
    ORIGIN_FOLDERS = (
        '/home/david/dev/backup/test/',
    )
