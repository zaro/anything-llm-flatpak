#!/user/bin/python
import urllib.request
import email.utils
import xml.etree.ElementTree as ET

check_version_url = "https://s3.us-west-1.amazonaws.com/public.useanything.com/latest/version.txt"
f = urllib.request.urlopen(check_version_url)
last_modified_tuple = email.utils.parsedate(f.info()['Last-Modified'])
version = f.read().decode('ascii')
last_modified = f"{last_modified_tuple[0]}-{last_modified_tuple[1]:02}-{last_modified_tuple[2]:02}"
latest = (version, last_modified)

app_stream = ET.parse('com.useanything.AnythingLLMDesktop.metainfo.xml')
releases = []
for r in app_stream.findall("releases/release"):
    releases.append(
        (r.attrib["version"], r.attrib["date"])
    )
releases.sort(key=lambda e: e[1], reverse=True)

print("Latest:", latest)
print("Current:", releases[0])
