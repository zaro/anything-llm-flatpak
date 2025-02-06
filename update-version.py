#!/user/bin/python
import subprocess
import urllib.request
import re
import os
import email.utils
import hashlib
import json
import xml.etree.ElementTree


app_image_url = "https://cdn.anythingllm.com/latest/AnythingLLMDesktop.AppImage"
check_version_url = "https://cdn.anythingllm.com/latest/version.txt"
result = subprocess.run(['curl', '-si', check_version_url], stdout=subprocess.PIPE)
output_lines = result.stdout.decode().splitlines()
for line in output_lines:
    m = re.match('^last-modified: (.*)', line)
    if m:
        last_modified_str = m.group(1)
        break

if not last_modified_str:
    print("Failed to get last-modified")
    exit(1)

last_modified_tuple = email.utils.parsedate(last_modified_str)
latest_version = output_lines[-1].strip()
last_modified = f"{last_modified_tuple[0]}-{last_modified_tuple[1]:02}-{last_modified_tuple[2]:02}"
latest = (latest_version, last_modified)

app_stream_file = 'com.useanything.AnythingLLMDesktop.metainfo.xml'
app_stream = xml.etree.ElementTree.parse(app_stream_file)
releases = []
for r in app_stream.findall("releases/release"):
    releases.append(
        (r.attrib["version"], r.attrib["date"])
    )
releases.sort(key=lambda e: e[1], reverse=True)

print("Latest:", latest)
print("Current:", releases[0])
if latest == releases[0]:
    print("  Up to date!")
    exit(0)

print("Calcualte last release sha256...")
# Open the URL and read its content
app_image_sha256_hash = hashlib.sha256()

file_name = 'AnythingLLMDesktop.AppImage'
# Open the URL and read the content in chunks
result = subprocess.run(['curl', '-Lo', file_name, app_image_url], stdout=subprocess.PIPE)
with open(file_name, 'rb') as response:
    while True:
        chunk = response.read(1024 * 1024)
        if not chunk:
            break
        # Update the hash with the current chunk
        app_image_sha256_hash.update(chunk)
os.remove(file_name)
# Return the final hash as a hexadecimal string
latest_version_sha256 = app_image_sha256_hash.hexdigest()
print("Done.")

print("Update appstream")
new_release_element = xml.etree.ElementTree.SubElement(app_stream.findall("releases")[0], 'release')
new_release_element.attrib['type'] = 'stable'
new_release_element.attrib['version'] = latest[0]
new_release_element.attrib['date'] = latest[1]

app_stream.write(app_stream_file)

app_stream_sha256_hash = hashlib.sha256()

# Open the URL and read the content in chunks
with open(app_stream_file, 'rb') as f:
    while True:
        chunk = f.read(1024 * 1024)
        if not chunk:
            break
        # Update the hash with the current chunk
        app_stream_sha256_hash.update(chunk)

# Return the final hash as a hexadecimal string
app_stream_sha256 = app_stream_sha256_hash.hexdigest()
print("Done")

print("Generate sources.json")
with open("sources.json", "w") as f:
    json.dump([{
        "type": "file",
        "url": app_image_url,
        "sha256": latest_version_sha256
    }, {
        "type": "file",
        "path": app_stream_file,
        "sha256": app_stream_sha256
    }], fp=f, indent=2)
print("Done!")
