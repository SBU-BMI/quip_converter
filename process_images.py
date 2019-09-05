import sys
import subprocess
import ntpath
import os
import os.path
import pandas as pd

inp_folder="/data/images/"
out_folder="/data/output/"

convert_no_error = 0
convert_no_error_msg = "conversion-no-error"
convert_showinf_error = 1
convert_showinf_error_msg = "showinf-failed"
convert_fconvert_error = 2
convert_fconvert_error_msg = "fconvert-failed"
convert_vips_error = 3
convert_vips_error_msg = "vips-failed"

def convert_image(ffolder,fname):
    ierr_code = convert_no_error;
    ierr_msg  = convert_no_error_msg;
    base_name = ntpath.basename(fname);
    dest_folder = out_folder + fname + "/";
    
    if not os.path.exists(dest_folder):
       os.makedirs(dest_folder);
    fname_pre = os.path.splitext(base_name)[0];
    fname_tmp = fname_pre + "-bigtiff.tif";
    fname_out = fname_pre + "-multires.tif";
    cmd = "run_convert_wsi.sh " + ffolder + fname;
    cmd = cmd + " " + dest_folder + fname_tmp;
    cmd = cmd + " " + dest_folder + fname_out;

    process = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    process.wait()
    if process.returncode == 1:
       ierr_code = convert_showinf_error;
       ierr_msg  = convert_showinf_error_msg;
    if process.returncode == 2:
       ierr_code = convert_fconvert_error;
       ierr_msg  = convert_fconvert_error_msg;
    if process.returncode == 3:
       ierr_code = convert_vips_error;
       ierr_msg  = convert_vips_error_msg;

    return fname+"/"+fname_out,ierr_code,ierr_msg

def main(argv):
    inp_manifest = "manifest.csv"
    out_manifest = "out-manifest.csv"
    if len(argv)==1:
       inp_manifest = argv[0]
       out_manifest = "out-" + inp_manifest
    if len(argv)==2:
       inp_manifest = argv[0]
       out_manifest = argv[1]

    inp_file = open(inp_folder + "/" + inp_manifest);
    pf = pd.read_csv(inp_file,sep=',')
    if "path" not in pf.columns:
        print("ERROR: Header is missing in file: ",inp_manifest)
        inp_file.close()
        sys.exit(1);

    out_csv  = open(out_folder + "/" + out_manifest,"w");

    pf["convert_error_code"] = 0
    pf["convert_error_msg"]  = ""
    pf["original_filename"]  = ""
    for file_idx in range(len(pf["path"])):
        file_row = pf["path"][file_idx];
        print("Processing: ",file_row)

        converted_filename,ierr_code,ierr_msg = convert_image(inp_folder,file_row)
        pf.at[file_idx,"convert_error_code"] = ierr_code
        pf.at[file_idx,"convert_error_msg"] = ierr_msg 
        pf.at[file_idx,"original_filename"] = file_row
        pf.at[file_idx,"path"] = converted_filename

    pf.to_csv(out_csv,index=False)

    inp_file.close();
    out_csv.close();

if __name__ == "__main__":
   main(sys.argv[1:])

