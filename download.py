#!/usr/bin/python

import urllib2
import sys
from runprogram import runprogram

ORIGINAL_HOST = "217.118.160.67"
SERVE_HOST = "do.twinone.org:8000"
WORK_DIR = "out"
SERVE_FILE = "/var/www/out.mp4"

def get_url(token):
    return "http://217.118.160.67/10/v166/aes/adaptive/components/soaps/gtst/279883/" + token + ".ssm/" + token + ".m3u8"

def save(content, filename):
    file = open(filename, "w")
    file.write(content)

def is_link(line):
    return line.startswith("http://") or line.startswith("https://")

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

def get_padded_iv(seqnum):
    """ Initialization vectors consist of 16bytes (128 bit) expressed as 32 hex chars """
    h = hex(seqnum)[2:]
    return ("0" * (32-len(h))) + h


if len(sys.argv) >= 2:
    token = sys.argv[1]
else:
    token = raw_input("Enter token: ")

url = get_url(token)
# print url

content = urllib2.urlopen(url).read()
# save(content, "available-streams.m3u8.txt")
# save(content, "/var/www/available-streams.m3u8.txt")



def max_resolution(file):
    """
    Returns (max_string, link)
    max_string: Maximum resolution: WxH
    link:       Where the m3u8 file can be found
    """
    lines = file.split("\n")
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
    return max_str, lines[max_idx+1]

max_res = max_resolution(content)
print "Maximum available resolution: " + max_res[0]

url = replace_host(max_res[1], ORIGINAL_HOST)
content = urllib2.urlopen(url).read()

def num_ts_files(lines):
    lines = content.split("\n")
    max = 0
    link = False
    for line in lines:
        if not is_link(line) or not line.endswith(".ts"):
            continue
        if not link:
            link = replace_host(line, ORIGINAL_HOST)
            link = "-".join(link.split("-")[:-1]) + "-{{SEQ_NUM}}.ts"
        curr = int(line.split("-")[-1][:-3])
        if curr > max: max = curr
    return max, link

num_ts, ts_link = num_ts_files(content)

#print "Video url: " + ts_link
# print "Number of ts files: " + str(num_ts)

print ""
print "Downloading " + str(num_ts) + " parts..."
status, out, err = runprogram(["./download-parts.sh", ts_link, str(num_ts), WORK_DIR])
if status != 0:
    print "Error!: " + str(status)
    print out
    print err

dec_key = runprogram(["./key.sh", token])[1].strip()
print "Got decryption key: " + dec_key
print "Decrypting " + str(num_ts) + " files..."

for i in range(1, num_ts+1):
    infile = WORK_DIR + "/" + str(i) + ".ts"
    outfile = WORK_DIR + "/" + str(i) + ".dec.ts"
    dec_iv = get_padded_iv(i)
    runprogram(["./decrypt.sh", infile, outfile, dec_key, dec_iv])

print "All files decrypted"
print ""

print "Converting to mp4"
runprogram(["./convert.sh", WORK_DIR, str(num_ts), SERVE_FILE])

print ""
print "Done, now watch your video at http://do.twinone.org:8000/out.mp4"