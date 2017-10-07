
#with open('owncloud', 'r') as f:
#    cnt = f.read()
#
#dimport json

#data = json.loads(cnt)
#files = data['data']['files']
#tmpl = """curl 'http://cloud.dvdbng.com/index.php/core/ajax/share.php' -H 'Host: cloud.dvdbng.com' -H 'User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:41.0) Gecko/20100101 Firefox/41.0' -H 'Accept: */*' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'DNT: 1' -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'requesttoken: ' -H 'OCS-APIREQUEST: true' -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: http://cloud.dvdbng.com/index.php/apps/files/?dir=%%2FInstantUpload' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data ''"""
#for i, f in enumerate(files[98:474]):
#    print tmpl % f,
#    print ("&" if i%3 != 0 else "")

import owncloud
import re

DONT_SHARE_RE = re.compile('2015(0802_1247|0730_091411|0726_2350)')


def share_file(f):
    shares = oc.get_shares(f.path)
    is_shared = len(shares) > 0
    should_be_shared = not DONT_SHARE_RE.search(f.path)
    if is_shared and not should_be_shared:
        print "Shared but shouldn't"
        oc.delete_share(shares[0]['id'])
    elif not is_shared and should_be_shared:
        print "Not shared but should", f.path
        oc.share_file_with_group(f.path, 'family', perms=17)

oc = owncloud.Client('http://cloud.dvdbng.com/')
oc.login('bengoa', '') # XXX!!!
files = oc.list('/InstantUpload/')

files.sort(key=lambda file: file.get_last_modified())

def run():
    for file in files[-200:]:
        share_file(file)

run()

