#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  7 11:53:43 2022

@author: maggiecherney
"""
import pandas as pd
import geopandas as gpd
import json

print("started 02b_census_blocks.py")

specs = json.load( open('county.json') )
county_code = specs['geoid']

tl_2019_block_file = "tl_2019_37_tabblock10.zip"

blocks = pd.read_csv(f"census_blocks_{county_code}.csv")

output_file = f'blocks_{county_code}.gpkg'

#%%

# read in the NC 2019 geo block file 

geo_block_file = gpd.read_file(tl_2019_block_file)

# select the blocks in the county 

county_blocks = geo_block_file["GEOID10"].str.startswith(county_code)

# create a dataframe of the blocks in the county 

county_block_data = geo_block_file[county_blocks]

#%%

# join the 2019 block data onto the 2010 census block data 

merge = county_block_data.merge(blocks, 
                     right_on="geoid", 
                     left_on="GEOID10",
                     how="left",
                     indicator=True)

print(merge["_merge"].value_counts())

merge = merge.drop(columns = '_merge')

#%%

# only keep blocks where the population is greater than zero 

merge["pop"] = merge["pop"].astype(int)

pop = merge.query("pop > 0")

# write out the results as a gpkg

pop.to_file(output_file,layer="blocks",index=False)

print("finished 02_census_blocks.py")






