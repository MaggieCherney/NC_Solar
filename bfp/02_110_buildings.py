#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb  8 12:38:18 2022

@author: maggiecherney
"""
#%%

res_parcels = '110'
# NOTE: 110 is an NC specific parcel use code for year round residential homes

#%%

import geopandas as gpd

input_file = "merged.gpkg"
house_file = "110_buildings.gpkg"
house_csv = "110_buildings.csv"

bfp = gpd.read_file(input_file, layer="buildings")

#%% Identify the residential parcels 

print(bfp.info())

parcel_use = bfp["PARUSECODE"].value_counts()

# variable including residential parcel use codes 
#house_range = [res_parcels]

# data in PARUSECODE is stored as string variables 
# convert to float and check if float variable is in the house_range 
is_house = bfp["PARUSECODE"]==res_parcels

# optional print statement 
#print(is_house.value_counts())

house = bfp[is_house]
not_house = bfp[is_house==False]

# check to see if any values in not_house are in house_range 
check = not_house["PARUSECODE"].value_counts(sort=False)

#%% Check to see if any houses are not associated with a parcel 

# see how many houses didn't have a parcel 
# print the parcels within house and not_house that have parcel numbers 

print(house["PARNO"].describe())
print(not_house["PARNO"].describe())

#%% Write out the results to .gpkg and .csv files 

# remove the index_right column and rename the area column to roof_area
house = house.drop(columns="index_right")
house = house.rename(columns={"area":"roof_area"})

house.to_file(house_file, driver="GPKG", layer="buildings")
trim = house.drop(columns="geometry")
trim.to_csv(house_csv, index=False)
