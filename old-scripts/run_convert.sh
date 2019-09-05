#!/bin/bash

if [ $# -ne 3 ]; then
    echo "run_convert.sh <input folder> <manifest_file> <output folder>"
    exit 1
fi

inpfolder=$1
manifestf=$2
outfolder=$3
if [ ! -f "$manifestf" ]; then
   echo "File: " $manifestf "does not exist."
   exit 1
fi

if [ ! -d "$outfolder" ]; then
	mkdir -p $outfolder 
fi

idx=`head -n 1 $manifestf | awk -F ',' 'BEGIN {j=-1;} {for (i=1;i<=NF;i++) { if ($i=="path") { j=i; } }} END {print j}'`;
if [[ "$idx" == -1 ]]; then
	echo "Header is missing in file: " $manifestf 
 	exit 1;
fi

manifesto=$(basename $manifestf);
head -n 1 $manifestf > $outfolder/$manifesto
for i in `tail -n +2 $manifestf`; do 
 	echo $i;
 	pre_val=`echo $i | awk -v idx=$idx -F ',' '{for (i=1;i<idx;i++) printf "%s,",$i;}'`;
 	fname=`echo $i | awk -v idx=$idx -F ',' '{print $idx}'`;
 	post_val=`echo $i | awk -v idx=$idx -F ',' '{for (i=idx+1;i<=NF;i++) printf ",%s",$i}'`; 

	infolder=$(dirname "$fname")
	ffname=$(basename "$fname")
 	filename1="${ffname%.*}"
 	filename=${filename1// /-};
	if [ $infolder != "." ]; then
		if [ ! -d "$outfolder/$infolder" ]; then
			mkdir $outfolder/$infolder;
		fi
		mrfile="$outfolder/$infolder/$filename-multires.tif"
	else	
 		mrfile="$outfolder/$filename-multires.tif"
	fi
	mrname=$(basename $mrfile)
 	run_convert_wsi.sh "$inpfolder/$fname" "$mrfile"
	if [ $infolder != "." ]; then
		echo $pre_val""$infolder"/"$mrname""$post_val >> $outfolder/$manifesto
	else	
		echo $pre_val""$mrname""$post_val >> $outfolder/$manifesto
	fi

done

