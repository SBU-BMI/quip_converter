import sys
import subprocess
import ntpath
import os
import os.path
import pandas as pd
import argparse
import uuid

convert_no_error = 0
convert_no_error_msg = "conversion-no-error"
convert_showinf_error = 1
convert_showinf_error_msg = "showinf-failed"
convert_fconvert_error = 2
convert_fconvert_error_msg = "fconvert-failed"
convert_vips_error = 3
convert_vips_error_msg = "vips-failed"

def convert_image(ifname,file_uuid):
    ierr_code = convert_no_error
    ierr_msg  = convert_no_error_msg
    base_name = ntpath.basename(file_uuid)
    if not os.path.exists(file_uuid): 
        os.makedirs(file_uuid)
    fname_pre = os.path.splitext(base_name)[0]
    fname_tmp = file_uuid + "/" + fname_pre + "-bigtiff.tif"
    fname_out = file_uuid + "/" + fname_pre + "-multires.tif"
    cmd = "run_convert_wsi.sh " + ifname
    cmd = cmd + " " + fname_tmp
    cmd = cmd + " " + fname_out

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

    return fname_out,ierr_code,ierr_msg

parser = argparse.ArgumentParser(description="Convert WSI images to multires, tiff images.")
parser.add_argument("--inpmeta",nargs="?",default="quip_manifest.csv",type=str,help="input manifest (metadata) file.")
parser.add_argument("--outmeta",nargs="?",default="quip_manifest.csv",type=str,help="output manifest (metadata) file.")
parser.add_argument("--errfile",nargs="?",default="quip_wsi_error_log.json",type=str,help="error log file.")
parser.add_argument("--inpdir",nargs="?",default="/data/images",type=str,help="input folder.")
parser.add_argument("--outdir",nargs="?",default="/data/output",type=str,help="output folder.")

def main(args):
    inp_folder = args.inpdir
    out_folder = args.outdir
    inp_manifest_fname = args.inpmeta
    out_manifest_fname = args.outmeta 
    out_error_fname = args.errfile 

    out_error_fd = open(out_folder + "/" + out_error_fname,"w");
    all_log = {}
    all_log["error"] = []
    all_log["warning"] = [] 
    try:
        inp_metadata_fd = open(inp_folder + "/" + inp_manifest_fname);
    except OSError:
        ierr = {}
        ierr["error_code"] = 1
        ierr["error_msg"] = "missing manifest file: " + str(inp_manifest_fname);
        all_log["error"].append(ierr)
        json.dump(all_log,out_error_fd)
        out_error_fd.close()
        sys.exit(1)

    pf = pd.read_csv(inp_metadata_fd,sep=',')
    if "path" not in pf.columns:
        ierr = {}
        ierr["error_code"] = 2
        ierr["error_msg"] = "column path is missing."
        all_log["error"].append(ierr)
        json.dump(all_log,out_error_fd)
        out_error_fd.close()
        inp_metadata_fd.close() 
        sys.exit(1)

    if "file_uuid" not in pf.columns:
        iwarn = {}
        iwarn["warning_code"] = 1
        iwarn["warning_msg"] = "column file_uuid is missing. Will generate."
        all_log["warning"].append(iwarn)
        fp["file_uuid"] = "" 
        for idx, row in pf.iterrows(): 
            filename, file_extension = path.splitext(row["path"]) 
            pf.at[idx,"file_uuid"] = str(uuid.uuid1()) + file_extension
            
    if "row_status" not in pf.columns:
        iwarn = {}
        iwarn["warning_code"] = 3
        iwarn["warning_msg"] = "column row_status is missing. Will generate."
        all_log["warning"].append(iwarn)
        fp["row_status"] = "ok"
 
    out_metadata_fd  = open(out_folder + "/" + out_manifest_fname,"w")
    pf["original_filename"]  = ""
    for file_idx in range(len(pf["path"]))
        file_row = pf["path"][file_idx]
        file_uuid = pf["file_uuid"][file_idx]
        print("Processing: ",file_row)

        ifname = inp_folder+"/"+file_row
        ofname = out_folder+"/"+file_uuid
        converted_filename,ierr_code,ierr_msg = convert_image(ifname,ofname)
        if ierr_code != convert_no_error: 
            ierr = {} 
            ierr["error_code"] = ierr_code
            ierr["error_msg"] = ierr_msg 
            ierr["row_idx"] = file_idx
            ierr["filename"] = file_row 
            ierr["file_uuid"] = file_uuid
            all_log["error"].append(ierr) 
            if pf["row_status"][file_idx]=="ok": 
                pf.at[file_idx,"row_status"] = ierr_msg 
            else: 
                pf.at[file_idx,"row_status"] = pf["row_status"][file_idx]+";"+ierr_msg
        pf.at[file_idx,"original_filename"] = file_row
        pf.at[file_idx,"path"] = converted_filename

        one_row = pd.DataFrame(columns=pf.columns)
        tmp_row = pf.loc[file_idx,:]
        one_row = one_row.append(tmp_row)
        if file_idx == 0:
           one_row.to_csv(out_metadata_fd,mode="w",index=False)
        else:
           one_row.to_csv(out_metadata_fd,mode="a",index=False,header=False)

    json.dump(all_log,out_error_fd)

    inp_metadata_fd.close()
    out_metadata_fd.close()
    out_error_fd.close()
    sys.exit(0)

if __name__ == "__main__": 
    args = parser.parse_args(sys.argv[1:]); 
    main(args)
