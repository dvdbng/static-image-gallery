#!/bin/bash
set -e


cd "$(dirname "$0")"
git pull

python lowres_photos.py
python generate_index.py
python classify_images.py
python generate_index.py
