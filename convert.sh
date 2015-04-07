#!/bin/sh

if [ -z "$3" ]; then
	echo "Usage: $0 <work_dir> <num_files> <output_file>"
	exit 1
fi
WORK_DIR="$1"
NUM_FILES="$2"
OUT_FILE="$3"

cd "$WORK_DIR"
rm -f "$OUT_FILE"
for i in $(seq 1 "$NUM_FILES"); do
	cat "$i.dec.ts" >> "$OUT_FILE.ts"
	rm "$i.ts" "$i.dec.ts"
done

avconv -i "$OUT_FILE.ts" -acodec copy -vcodec copy "$OUT_FILE"

rm "$OUT_FILE.ts"