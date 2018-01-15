#!/bin/bash
LOCKFILE=/tmp/static_image_gallery_lock
if [ -e ${LOCKFILE} ] && kill -0 `cat ${LOCKFILE}`; then
    echo "already running"
    exit
fi

# make sure the lockfile is removed when we exit and then claim it
trap "rm -f ${LOCKFILE}; exit" INT TERM EXIT
echo $$ > ${LOCKFILE}

cd "$(dirname "$0")"
git pull

cp assets/* /home/owncloud/bengoa/files/photos/assets/

python lowres_photos.py && \
    python generate_index.py && \
    python classify_images.py && \
    python generate_index.py

rm -f ${LOCKFILE}
