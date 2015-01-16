#!/bin/sh

if [ -z "$4" ]; then
		echo "Usage: $0 <encrypted_file> <decrypted_file> <key> <iv>"
		exit 1
fi

openssl aes-128-cbc -d -in "$1" -out "$2" -K "$3" -iv "$4"