#!/bin/bash

# $1 = Download url. {{SEQ_NUM}} will be replaced with the sequence number
# $2 = num (number of items in the sequence, will always start from 1)
# $3 (optional) working directory (default=out)

if [ -z  "$2" ]; then
	echo "Usage: $0 <url> <num_parts> [work_dir]"
	exit 1
fi

if [ -n "$3" ]; then
	WORK_DIR="$3"
else
	WORK_DIR="out"
fi

mkdir -p "$WORK_DIR"
rm -rf "$WORK_DIR/*"

URL="$1"

for i in $(seq 1 $2); do
	dl_url="$(echo $URL|sed "s/{{SEQ_NUM}}/$i/g")"
	curl --silent "$dl_url" -o "$WORK_DIR/$i.ts" &
done

wait
