#!/bin/bash

if [ $# -eq 0 ]; then
    echo "run_convert.sh <input image> <output bigtif image> <output multires image>"
    exit 1
fi

export TMPDIR=/tmp

inp_img="$1"
tmp_img="$2"
out_img="$3"

read_val=`showinf -nopix -omexml-only -novalid "$inp_img" | grep Phys | awk -f $PROCAWKDIR/process.awk`;
if [ "$?" != "0" ]; then
	exit 1;
fi

s_idx=`echo $read_val | awk -F ',' '{print $1}'`;
mpp_x=`echo $read_val | awk -F ',' '{print $2}'`;
mpp_y=`echo $read_val | awk -F ',' '{print $3}'`;

bfconvert -bigtiff -compression LZW -series $s_idx "$inp_img" "$tmp_img"
if [ "$?" != "0" ]; then
	exit 2;
fi

# get pixel resolution in centimeters
cres_x=`echo "10000/$mpp_x" | bc -l`
cres_y=`echo "10000/$mpp_x" | bc -l`

vips openslideload "$tmp_img" "$out_img"[compression=jpeg,Q=90,xres=$cres_x,yres=$cres_y,tile,bigtiff,pyramid] 
if [ "$?" != "0" ]; then
	exit 3;
fi
exit 0;
