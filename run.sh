#!/bin/bash

#set -x

# Uncomment the following to run for REAL
# dry_run="--dry-run"

if ! [ "$1" ] || ! [ "$2" ]
then
	echo "Usage: $0 src dst"
	exit 1
fi

./backup.py $1 $2
rsync $dry_run -aruPzH --exclude-from=files_list.txt $1/ $2
