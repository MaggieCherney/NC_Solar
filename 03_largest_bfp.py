#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 15:22:02 2022

@author: maggiecherney
"""

import geopandas as gpd
import json 

specs = json.load( open('county.json') )
county_code = specs['geoid']

buildings_file = f"merged_bfp_parcels_{county_code}.gpkg"

output_file = f"largest_buildings_{county_code}.gpkg"

#%% Sort the buildings and select the largest building on each parcel

buildings = gpd.read_file(buildings_file, layer='buildings')

sort_buildings = buildings.sort_values(["PARNO","area"])
groups = sort_buildings.groupby("PARNO")
largest = groups.last()
largest["building_count"]=groups.size()

#%% Write out the results 

largest.to_file(output_file,layer="buildings",index=False)

