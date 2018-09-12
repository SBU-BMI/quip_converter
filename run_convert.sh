#!/bin/bash

if [ $# -eq 0 ]; then
    echo "run_convert.sh <input folder>"
    exit 1
fi

folder=$1
if [ ! -d "$folder" ]; then
   echo "Folder: " $inp_folder "does not exist."
   exit 1
fi
mkdir -p $folder/converted

find $folder -iname "*.vsi" | while read i
do
	echo $i;
        fname="$(basename "$i")"
	filename1="${fname%.*}"
	filename=${filename1// /-};
	mrfile="$folder/converted/$filename-multires.tif"
	btfile="$folder/converted/$filename-bigtiff.tif"
	run_convert_wsi.sh "$i" "$btfile" "$mrfile"
done
