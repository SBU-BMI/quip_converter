#!/bin/bash

if [ $# -eq 0 ]; then
    echo "run_convert.sh <input image> <output bigtif image> <output multires image>"
    exit 1
fi

export TMPDIR=$VIPS_TMPDIR

inp_img="$1"
tmp_img="$2"
out_img="$3"

read_val=`showinf -nopix -omexml-only -novalid "$inp_img" | grep Phys | awk -f $PROCAWKDIR/process.awk`;
s_idx=`echo $read_val | awk -F ',' '{print $1}'`;
mpp_x=`echo $read_val | awk -F ',' '{print $2}'`;
mpp_y=`echo $read_val | awk -F ',' '{print $3}'`;

echo "FILE: " "$inp_img" " ID: " $s_idx " MPP: " $mpp_x "x" $mpp_y

bfconvert -bigtiff -compression LZW -series $s_idx "$inp_img" "$tmp_img"	
vips tiffsave "$tmp_img" "$out_img" --compression=lzw --tile --tile-width=256 --tile-height=256 --pyramid --bigtiff

