#!/bin/bash
if [ $# -eq 0 ]; then
    echo "run_convert.sh <input image> <output image>"
    exit 1
fi
inp_img="$1"
out_img="$2"
export BF_MAX_MEM="4G"
read_val=`showinf -nopix -omexml-only -novalid "$inp_img" | grep Phys | awk -f $PROCAWKDIR/process.awk`;
s_idx=`echo $read_val | awk -F ',' '{print $1}'`;
mpp_x=`echo $read_val | awk -F ',' '{print $2}'`;
mpp_y=`echo $read_val | awk -F ',' '{print $3}'`;
echo "FILE: " "$inp_img" " ID: " $s_idx " MPP: " $mpp_x "x" $mpp_y
bfconvert -bigtiff -tilex 256 -tiley 256 -no-upgrade -compression LZW -pyramid-scale 2 -pyramid-resolutions 7 -series $s_idx "$inp_img" "$out_img"	
