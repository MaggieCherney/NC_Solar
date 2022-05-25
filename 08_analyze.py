#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Apr 11 20:54:48 2022

@author: maggiecherney
"""

import pandas as pd
import geopandas as gpd
import json

specs_c = json.load( open('county.json') )
county_code = specs_c['geoid']
specs_s = json.load( open('NC_info.json') )
ej_inc_cutoff = specs_s['ej_inc_cutoff']
ej_race_cutoff = specs_s['ej_race_cutoff']

input_file = f"census-acs-bgs-{county_code}.csv"

house_file = f"houses_by_block_{county_code}.gpkg"

bgs = pd.read_csv(input_file,dtype={"geoid":str})
houses = gpd.read_file(house_file, layer="bgs")

#%%

# define the usable percent of houses as those built after 1950 

old_houses = (bgs["B25034_011E"]+bgs["B25034_010E"]).sum()

print(f"\nnumber of old houses: {old_houses}")

total_houses = bgs["B25034_001E"].sum()

print(f"\ntotal number of houses: {total_houses}")

pct_old = old_houses/total_houses

pct_usable = 1-pct_old

print(f"\npercent of usable houses: {pct_usable}")

#%%

# apply the usable percent to the area and kw variables 

houses["usable_area"] = houses["area"]*pct_usable

print(houses["usable_area"].sum())

houses["usable_kw"] = houses["kw"]*pct_usable

print(houses["usable_kw"].sum())

#%%

# pct nonwhite by block group 
trim = bgs[["geoid","B02001_002E","B02001_001E","B19013_001E"]]
trim = trim.rename(columns = {"B02001_002E":"white_pop",
                              "B02001_001E":"total_pop",
                              "B19013_001E":"median_inc",
                              "geoid":"GEOID"})

houses = houses.merge(trim,on="GEOID",validate="1:1",how="outer")

pct_nonwhite_bg = 1-(houses["white_pop"]/houses["total_pop"])

pct_nonwhite_bg = pct_nonwhite_bg.dropna()

houses["ej_race"] = ""
houses["ej_race"] = houses["ej_race"].where(pct_nonwhite_bg < ej_race_cutoff,"R")

#%%

houses["ej_inc"] = ""
houses["ej_inc"] = houses["ej_inc"].where(houses["median_inc"] > ej_inc_cutoff,"E")

#%%

houses["ej_flag"] = houses["ej_race"]+houses["ej_inc"]


#%%

# calculate mean kW per house by block group 

houses["mean_kw"] = houses["usable_kw"]/houses["count"]

#%%

grouped = houses.groupby("ej_flag")

total_kw = grouped[["usable_kw","total_pop"]].sum()
total_kw["kw_pct"] = total_kw["usable_kw"]/total_kw["usable_kw"].sum()*100
total_kw["pop_pct"] = total_kw["total_pop"]/total_kw["total_pop"].sum()*100

total_kw["county"] = county_code

total_kw.to_csv(f"county/summary_{county_code}.csv")

#%%

houses.to_file(f"county/houses_{county_code}.gpkg",layer="bgs",index=False)

#%%

houses = houses.drop(columns="geometry")

houses.to_csv(f"county/full_{county_code}.csv")

print("finished 08_analyze.py")




 







