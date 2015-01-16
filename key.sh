#!/bin/sh

if [ -z "$1" ]; then
	echo "Usage: $0 <video_uuid>"
	exit 1
fi

VIDEO_UUID=$1

curl --silent "http://drm.rtl.nl/PlayReady/SoftDRMInternal.xml?uuid=${VIDEO_UUID}&drm=aes&version=666" | xxd -p