#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 13:34:54 2022

@author: maggiecherney
"""

import geopandas as gpd
import json 

specs = json.load( open('county.json') )
county_code = specs['geoid']
county_name = specs['name']

building_file = f"bfp_{county_code}.gpkg"
parcel_file = f"parcels/{county_name}_parcels.zip!nc_{county_name}_parcels_poly.shp"

output_file = f"merged_bfp_parcels_{county_code}.gpkg"
#%%

poly = gpd.read_file(parcel_file)
poly = poly.to_crs(epsg=32617)

#%%

bfp = gpd.read_file(building_file,driver="GPKG",layer="buildings")
bfp = bfp.to_crs(epsg=32617)
bc = bfp.centroid
ba = bfp.area

areas = gpd.GeoDataFrame(data=ba, geometry=bc)
areas = areas.rename(columns={0:"area"})

#%%

merged = gpd.sjoin(areas, poly, how='left')
merged.to_file(output_file,layer="buildings",index=False)

print("finished 03_merge_bfp_parcel.py")