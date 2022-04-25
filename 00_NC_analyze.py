#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 15 12:23:12 2022

@author: maggiecherney
"""

import pandas as pd
import numpy as np
import json


input_file = "census-acs-bgs-NC.csv"

nc_bgs = pd.read_csv(input_file)

#%%

# find the percent of people of color in NC

total = nc_bgs["B02001_001E"].sum()
print(f"\ntotal pop: {total}")

white = nc_bgs["B02001_002E"].sum()
print(f"\nwhite: {white}")

pct_white = white/total
print(f"\npercent white: {pct_white}")

pct_nonwhite = 1-pct_white
print(f"\npercent nonwhite: {pct_nonwhite}")

# 31% people of color 

# pct nonwhite by block group 

pct_nonwhite_bg = 1-(nc_bgs["B02001_002E"]/nc_bgs["B02001_001E"])

pct_nonwhite_bg = pct_nonwhite_bg.dropna()

nonwhite_quintiles = np.percentile(pct_nonwhite_bg,[0,20,40,60,80])

# 80th percentile = 55%

print(nonwhite_quintiles)

#%%

nc_bgs = nc_bgs.replace({-666666666:np.nan})

# find the lowest quintile for median income 

inc = nc_bgs["B19013_001E"].dropna()

inc_quintiles = np.percentile(inc,[0,20,40,60,80])

print(inc_quintiles)

#%%

info = {
        "ej_inc_cutoff":round(inc_quintiles[1],-3),
        "ej_race_cutoff":round(nonwhite_quintiles[-1],2)
        }
fh = open("NC_info.json","w")
json.dump(info,fh,indent=4)
fh.close()









