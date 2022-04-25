#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:19:56 2022

@author: maggiecherney
"""
import pandas as pd
import geopandas as gpd
import json

specs = json.load( open('county.json') )
county_code = specs['geoid']
county_fips_code = specs['county_fips_code']

input_file = f"merged_bfp_blocks_{county_code}.gpkg"
block_file = f"blocks_{county_code}.gpkg"
bgs_file = "tl_2019_37_bg.zip"

output_file = f"houses_by_block_{county_code}.gpkg"

houses = gpd.read_file(input_file, dtype={"area":int})
block_geo = gpd.read_file(block_file)


#%%

# filter the building footprint data to buildings less than 500

houses_500 = houses.query("area <= 500").copy()

#%% 

# create a new variable that is equal to 25% of the roof area for each house

houses_500['usable'] = houses_500['area']*0.25

# create a new variable that estimates the kw capacity per roof 

houses_500['kw'] = houses_500['usable']*(4/25)


#%%

# group the houses by block and then count the number of houses in each block 
# and add together their area

house_groups = houses_500.groupby("GEOID10")
blocks = pd.DataFrame()

blocks["count"] = house_groups.size()

blocks["area"] = house_groups["area"].sum()

blocks["kw"] = house_groups["kw"].sum()

# merge blocks onto block_geo using the geoid 

merged = block_geo.merge(blocks,on="GEOID10",how="left",indicator=True)

print(merged["_merge"].value_counts())

# replace missing values that were only in the house dataframe wth zero 

for columns in ["kw","area","count"]:
    merged[columns] = merged[columns].where( merged['_merge']=='both', 0 )
    
merged = merged.drop(columns = '_merge')

# write out the results 

houses_500.to_file(output_file,layer="houses")
merged.to_file(output_file,layer="blocks")

#%%

# filter the census bg file to the county using the county fips code

# read in the NC 2019 bgs file

block_groups = gpd.read_file(bgs_file)

# select the bgs in the county 

county_bgs = block_groups["COUNTYFP"].str.startswith(county_fips_code)

# create a dataframe of the county bgs

county_bgs = block_groups[county_bgs]


#%%

# create a new layer for the block groups 

houses_500['bg'] = houses_500['GEOID10'].str[:12]

bgs_grouped = houses_500.groupby('bg')

bgs = pd.DataFrame()

bgs["count"] = bgs_grouped.size()

bgs["area"] = bgs_grouped["area"].sum()

bgs["kw"] = bgs_grouped["kw"].sum()

# merge bgs onto block_geo using the geoid 

bgs_merged = county_bgs.merge(bgs,left_on="GEOID",right_on="bg",how="left",indicator=True)

print(bgs_merged["_merge"].value_counts())

# replace missing values that were only in the house dataframe wth zero 

for columns in ["kw","area","count"]:
    bgs_merged[columns] = bgs_merged[columns].where( bgs_merged['_merge']=='both', 0 )
    
bgs_merged = bgs_merged.drop(columns = '_merge')

# write out the results as the bgs layer 

bgs_merged.to_file(output_file,layer="bgs")












