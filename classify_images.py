from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os.path
import re
import sys
import subprocess
import json
import time

from config import DST_FOLDER

def data_file_for(image):
  return os.path.splitext(image)[0] + '.json'

def main():
  with open(os.path.join(DST_FOLDER, 'index.json'), 'r') as f:
    photo_map = json.loads(f.read())

  for orig, image in photo_map.iteritems():
    if os.path.exists(data_file_for(image)):
      continue
    print('Infer %s' % image)
    subprocess.call(['python', 'classify_image.py', image])
    time.sleep(15)


if __name__ == '__main__':
    main()

