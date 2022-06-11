 #!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:34:04 2022

@author: maggiecherney
"""

import geopandas as gpd
import json

print("started 05_merge_bfp_blocks.py")

specs = json.load( open('county.json') )
county_code = specs['geoid']

largest_bfp = f"largest_buildings_{county_code}.gpkg"
blocks = f"blocks_{county_code}.gpkg"

output_file = f"merged_bfp_blocks_{county_code}.gpkg"

#%%

# read in the bfp_parcels gpkg 

bfp = gpd.read_file(largest_bfp,driver="GPKG",layer="buildings")

# drop the "index_right" column from bfp

bfp = bfp.drop(columns="index_right")

# read in the blocks gpkg

blocks = gpd.read_file(blocks,driver="GPKG", layer="blocks")

# drop all columns but the GEOID from the block data 

block_geoid = blocks[['GEOID10','geometry']]
block_geoid = block_geoid.to_crs(epsg=32617)

#%%

# merge the bfp and block files 

merged = gpd.sjoin(bfp, block_geoid, how='left')

merged.to_file(output_file,layer="buildings",index=False)

print("finished 05_merge_bfp_blocks.py")



