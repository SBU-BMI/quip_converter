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
find $folder -iname "*.$extension" | while read i
do
	echo $i;
	fname="$(basename "$i")"
	filename1="${fname%.*}"
	filename=${filename1// /-};
	mrfile="$folder/$filename-multires.tif"
	tmpfile="$folder/$filename-big.tif"
	run_convert_wsi.sh "$i" "$tmpfile" "$mrfile"
done
