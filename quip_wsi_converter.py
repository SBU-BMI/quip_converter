import sys
import subprocess
import ntpath
import os
import os.path
import pandas as pd
import argparse
import uuid
import json

error_info = {}
error_info["no_error"] = { "code":0, "msg":"no-error" }
error_info["missing_file"] = { "code":301, "msg":"input-file-missing" }
error_info["file_format"] = { "code":302, "msg":"file-format-error" }
error_info["missing_columns"] = { "code":303, "msg":"missing-columns" }
error_info["showinf_failed"] = { "code":304, "msg":"showinf-failed" }
error_info["fconvert_failed"] = { "code":305, "msg":"fconvert-failed" }
error_info["vips_failed"] = { "code":306, "msg":"vips-failed" }

def convert_image(ifname,file_uuid):
    ierr = error_info["no_error"]
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
        ierr = error_info["showinf_failed"]
    if process.returncode == 2:
        ierr = error_info["fconvert_failed"]
    if process.returncode == 3:
        ierr = error_info["vips_failed"]

    return fname_out,ierr

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
        ierr = error_info["missing_file"]
        ierr["msg"] = ierr["msg"]+": " + str(inp_manifest_fname);
        all_log["error"].append(ierr)
        json.dump(all_log,out_error_fd)
        out_error_fd.close()
        sys.exit(1)

    pf = pd.read_csv(inp_metadata_fd,sep=',')
    if "path" not in pf.columns:
        ierr = error_info["missing_columns"]
        ierr["msg"] = ierr["msg"]+ ": "+ "path."
        all_log["error"].append(ierr)
        json.dump(all_log,out_error_fd)
        out_error_fd.close()
        inp_metadata_fd.close() 
        sys.exit(1)

    if "file_uuid" not in pf.columns:
        iwarn = error_info["missing_columns"]
        iwarn["msg"] = iwarn["msg"]+": "+"file_uuid. Will generate."
        all_log["warning"].append(iwarn)
        fp["file_uuid"] = "" 
        for idx, row in pf.iterrows(): 
            filename, file_extension = path.splitext(row["path"]) 
            pf.at[idx,"file_uuid"] = str(uuid.uuid1()) + file_extension
            
    if "error_code" not in pf.columns:
        iwarn = error_info["missing_columns"]
        iwarn["msg"] = iwarn["msg"]+": "+"error_code. Will generate."
        all_log["warning"].append(iwarn)
        fp["error_code"] = str(error_info["no_error"]["code"]) 

    if "error_msg" not in pf.columns:
        iwarn = error_info["missing_columns"]
        iwarn["msg"] = iwarn["msg"]+": "+"error_msg. Will generate."
        all_log["warning"].append(iwarn)
        fp["error_msg"] = error_info["no_error"]["msg"] 
 
    out_metadata_fd  = open(out_folder + "/" + out_manifest_fname,"w")
    pf["original_filename"]  = ""
    for file_idx in range(len(pf["path"]))
        file_row = pf["path"][file_idx]
        file_uuid = pf["file_uuid"][file_idx]
        print("Processing: ",file_row)

        ifname = inp_folder+"/"+file_row
        ofname = out_folder+"/"+file_uuid
        converted_filename,ierr = convert_image(ifname,ofname)
        if str(ierr["code"]) != str(error_info["no_error"]["code"]):
            ierr["row_idx"] = file_idx
            ierr["filename"] = file_row 
            ierr["file_uuid"] = file_uuid
            all_log["error"].append(ierr) 
            if str(pf["error_code"][file_idx])==str(error_info["no_error"]["code"]): 
                pf.at[file_idx,"error_code"] = str(ierr["code"]) 
                pf.at[file_idx,"error_msg"] = ierr["msg"] 
            else: 
                pf.at[file_idx,"error_code"] = str(pf.at[file_idx,"error_code"])+";"+str(ierr["code"]) 
                pf.at[file_idx,"error_msg"] = pf.at[file_idx,"error_msg"]+";"+ierr["msg"] 
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
