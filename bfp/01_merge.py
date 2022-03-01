#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  4 13:21:51 2022

@author: maggiecherney
"""
#%%

import geopandas as gpd

building_file = "../Data/bfp_37157.gpkg"
parcel_file = "../Data/rockingham_parcels/nc_rockingham_parcels_poly.shp"
point_file = "../Data/rockingham_parcels/nc_rockingham_parcels_pt.shp"

output_file = "merged.gpkg"

#%% Read and reproject the parcel file 

poly = gpd.read_file(parcel_file)
poly = poly.to_crs(epsg=32617)

# #%% Check point file

# pt = gpd.read_file(point_file)

# check = zip(sorted(poly.columns), sorted(pt.columns))
# for c1,c2 in check:
#     if c1!=c2:
#         print(c1,c2)

#%% Merge the bfp centroid and area data

bfp = gpd.read_file(building_file,driver="GPKG",layer="buildings")
bfp = bfp.to_crs(epsg=32617)
bc = bfp.centroid
ba = bfp.area

areas = gpd.GeoDataFrame(data=ba, geometry=bc)
areas = areas.rename(columns={0:"area"})

areas.to_file("areas.gpkg", driver="GPKG", layer="area")

#%% Write out the results to a .gpkg file 

merged = gpd.sjoin(areas, poly, how='left')
merged.to_file(output_file, driver="GPKG", layer="buildings")
