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

for i in `find $folder -name "*.vsi" -print`; do 
	echo $i;
        fname="$(basename $i)"
	filename="${fname%.*}"
	mrfile="$folder/converted/$filename-multires.tif"
	btfile="$folder/converted/$filename-bigtiff.tif"
	run_convert_wsi.sh $i $btfile $mrfile
done
