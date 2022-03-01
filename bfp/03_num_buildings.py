#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Feb 15 13:12:45 2022

@author: maggiecherney
"""
#%%

import geopandas as gpd

raw = gpd.read_file('110_buildings.gpkg', layer='buildings')

#%%

by_code = raw['PARUSECODE'].value_counts()
print(by_code)

#%% Determine the number of buildings on each parcel 

# database query to pick out where the fields have 110 as the value
# trim = raw.query('PARUSECODE=="110"')

grp = raw.groupby('PARNO')
num_buildings = grp.size()
print(num_buildings.value_counts())

#%% Merge the number of buildings onto the parcel file 

num_buildings.name = 'num_buildings'

merge = raw.merge(num_buildings,left_on='PARNO',right_index=True,
                  how='outer',validate='m:1',indicator=True)

print(merge['_merge'].value_counts())

#%% Write out the results as a .gpkg file

merge = merge.drop(columns="_merge")

# create a gpkg that includes the number of buildings on each parcel 
# as a parcel attribute 
merge.to_file('num_buildings.gpkg', driver="GPKG", layer="num_buildings")
