#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon May 16 16:16:56 2022

@author: maggiecherney
"""

import subprocess
import os
import json
import pandas as pd
#import sys
cmd = "./process_county.sh"
cfile = "tl_2019_us_county.zip"
temp_prefixes = ['bfp','blocks','houses_by_block',
                 'largest_buildings','merged_bfp_blocks',
                 'merged_bfp_parcels']
nc_counties = pd.read_csv("nc_counties.csv",dtype=str)
nc_counties = nc_counties.to_dict(orient="records")
# counties = [
#     {"geoid":"37001","name":"alamance"},
#     {"geoid":"37157","name":"rockingham"},
#     {"geoid":"37125","name":"moore"}
#     ]
#%%
for cinfo in nc_counties[:100]:
    print(cinfo["name"],flush=True)
    c = cinfo["geoid"]
    temp_files = [f'{pre}_{c}.gpkg' for pre in temp_prefixes]
    cinfo["cfile"] = cfile
    fh = open("county.json","w")
    json.dump(cinfo,fh,indent=4)
    fh.close()
    sname = f"county/full_{c}.csv"
    if os.path.exists(sname):
        continue 
    proc = subprocess.run([cmd,c],capture_output=True,text=True)
    print(proc.stdout)
    fh = open(f"county/log_{c}.txt","w")
    fh.write(proc.stdout)
    fh.close()
    assert proc.returncode==0
    lines = proc.stdout.split("\n")
    lastline = lines[-2]
    if not lastline.startswith("finished 08"):
        print("failed")
        break 
    else:
        for temp in temp_files:
            os.remove(temp)