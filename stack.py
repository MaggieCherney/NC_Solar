#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun  8 15:47:11 2022

@author: maggiecherney
"""

import geopandas as gpd
import pandas as pd 
import os 
import shutil
import numpy as np

files = [f for f in os.listdir("county") if f.startswith("full")]

state = pd.DataFrame()
for f in files:
    county = pd.read_csv("county/"+f, dtype={"GEOID":str})
    state = pd.concat([state,county],axis="index",ignore_index=True)
    
state = state.drop(columns=['Unnamed: 0','NAMELSAD', 'MTFCC', 'FUNCSTAT',
                            'ALAND', 'AWATER','INTPTLAT','INTPTLON','STATEFP',
                            'COUNTYFP', 'TRACTCE', 'BLKGRPCE'])

state.to_csv("state.csv",index=False)

#%%

bgs = gpd.read_file("tl_2019_37_bg.zip")

merged = bgs.merge(state,on="GEOID",validate="1:1",indicator=True)

print(merged["_merge"].value_counts())

merged = merged.drop(columns='_merge')

#%%

counties = gpd.read_file("tl_2019_us_county.zip")

counties = counties.query("STATEFP=='37'")

counties = counties[["COUNTYFP","NAME"]]

merged = merged.merge(counties,on="COUNTYFP",validate="m:1",indicator=True)

print(merged["_merge"].value_counts())

merged = merged.drop(columns='_merge')

#%%
merged = merged.query("ALAND>0")
has_pop = merged["total_pop"]>0
merged["ej_flag"] = merged["ej_flag"].where(merged["ej_flag"].notna(),"none")
merged["ej_flag"] = merged["ej_flag"].where(has_pop,"none")
merged["ej_race"] = merged["ej_race"].where(has_pop,"none")
merged["ej_inc"] = merged["ej_inc"].where(has_pop,"none")
stem = "state"

merged["inc_str"] = merged["median_inc"].apply(lambda x: "{:,}".format(x))
merged["inc_str"] = merged["inc_str"].where(merged["median_inc"]>0,"NA")

merged["pct_poc"] = (1-merged["white_pop"]/merged["total_pop"])*100
merged["pct_poc"] = merged["pct_poc"].fillna(0)

merged["mw"] = merged["usable_kw"]/1000

merged.to_file(stem,layer="solar",index=False)

shutil.make_archive(stem,"zip",stem)

shutil.rmtree(stem)