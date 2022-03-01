#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 22 13:13:03 2022

@author: maggiecherney
"""
#%%

import geopandas as gpd

buildings = gpd.read_file('110_buildings.gpkg', layer='buildings')

#%% Sorting buildings and selecting the largest building on each parcel 

sort_buildings = buildings.sort_values(["PARNO","roof_area"])
groups = sort_buildings.groupby("PARNO")
largest = groups.last()
largest["building_count"]=groups.size()

#%% Checking building selection 

# Double check to make sure the script is picking out the largest building 
# find a parcel that has more than one buildings and look at the 
# buildings dataset and look at the parcel number that has mutliple buildings 
# go through pick a few of the parcels numbers that have multiple bulidings 
# and write a select 
# Compare keepers to check to make sure that the buildings selected
# are in fact the largest 

three_building_parnos = ["894900281767","894300138806",
                         "803100330017","891307793301"]
keepers = largest.loc[three_building_parnos]
check = sort_buildings[sort_buildings["PARNO"].isin(three_building_parnos)]

#%% Write out the results to .gpkg and .csv files

largest.to_file("largest_buildings.gpkg", driver="GPKG", layer="buildings")
trim = largest.drop(columns="geometry")
trim.to_csv("largest_buildings.csv")

# try to run the sequence of scripts on another county 