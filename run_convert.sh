#!/bin/bash

if [ $# -ne 2 ]; then
    echo "run_convert.sh <input folder> <file extension>"
    exit 1
fi

folder=$1
extension=$2
if [ ! -d "$folder" ]; then
   echo "Folder: " $inp_folder "does not exist."
   exit 1
fi
mkdir -p $folder/converted
find $folder -iname "*.$extension" | while read i
do
	echo $i;
	fname="$(basename "$i")"
	filename1="${fname%.*}"
	filename=${filename1// /-};
	mrfile="$folder/converted/$filename-multires.tif"
	tmpfile="$folder/converted/$filename-tmp.tif"
	run_convert_wsi.sh "$i" "$tmpfile" "$mrfile"
done
