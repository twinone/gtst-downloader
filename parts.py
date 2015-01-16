#!/usr/bin/python

import urllib2
import sys
from subprocess import call

ORIGINAL_HOST = "217.118.160.67"
SERVE_HOST = "do.twinone.org:8000"

def get_url(token):
    return "http://217.118.160.67/10/v166/aes/adaptive/components/soaps/gtst/279883/" + token + ".ssm/" + token + ".m3u8"

def save(content, filename):
    file = open(filename, "w")
    file.write(content)

def is_link(line):
    return line.startswith("http://") or line.startswith("https://")

def is_drm(line):
    return line.startswith("#EXT-X-KEY")

def get_resolution(line):
    chunks = line.split(',')
    for chunk in chunks:
        data = chunk.split('=')
    if data[0] == 'RESOLUTION':
        return data[1]
    return False

def res_pixels(res):
    r = res.split('x')
    return int(r[0]) * int(r[1])

def replace_host(link, newhost):
    idx = 2 if is_link(link) else 0
    link_split = link.split("/");
    link_split[idx] = newhost
    return "/".join(link_split)


if len(sys.argv) >= 2:
    token = sys.argv[1]
else:
    token = raw_input("Enter token: ")

url = get_url(token)
print url

content = urllib2.urlopen(url).read()
lines = content.split("\n")
save(content, "available-streams.m3u8.txt")
save(content, "/var/www/available-streams.m3u8.txt")


max = 0
max_str = ""
max_idx = -1
for i in range(0, len(lines)):
    line = lines[i]
    if is_link(line):
        continue
    res = get_resolution(line)
    if not res:
        continue
    res_px = res_pixels(res)
    if res_px > max:
        max = res_px
        max_str = res
        max_idx = i

print "Maximum available resolution: " + str(max_str)



url = lines[max_idx+1]
url = replace_host(url, ORIGINAL_HOST)
# url now contains the biggest stream
# print url

content = urllib2.urlopen(url).read()
save (content, "parts.m3u8.txt")
save (content, "/var/www/parts.m3u8.txt")

lines = content.split("\n")

# now get the number of ts files that are in the file

def process_line(line):
    if is_drm(line):
        return False

    if not is_link(line):
        return line

    return "http://" + SERVE_HOST + "/out/" + line.split("-")[-1]

new_lines = []
for line in lines:
    l = process_line(line)
    if l != False:
        new_lines.append(l) 

content = "\n".join(new_lines)
save(content, "/var/www/parts-nodrm.m3u8.txt")
save(content, "/var/www/parts-nodrm.m3u8")




