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
find $folder -name "*.$extension" | while read i
do
	echo $i;
        filename=${i/.$2/};
        filename=${filename// /-};
        mrfile="$filename-multires.tif"
        tmpfile="$filename-big.tif"
	run_convert_wsi.sh "$i" "$tmpfile" "$mrfile"
done
