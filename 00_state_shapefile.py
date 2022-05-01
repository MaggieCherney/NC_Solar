"""
state_shapefile.py
Oct 2021 PJW
Author: Peter Wilcoxen 

Read one of Microsoft's building footprint files, which are in 
geojson format and slow to load, and convert it to a shapefile. 
"""

import geopandas as gpd
import json
import shutil 

#
#  Collect information about the input and output files from a 
#  small JSON file:
#
#     ms_file = name of MS geojson file for the state of interest
#     shp_file = name of output shapefile
#

spec = json.load( open('state.json') )

ms_file = spec['ms_file']
ostem = spec['shp_file'].replace('.zip','')

#
#  Now do the actual work. The shapefile will be an unzipped
#  subdirectory.
#

print( "reading...", flush=True )
g = gpd.read_file( ms_file )

print( "writing...", flush=True )
g.to_file( ostem )

#
#  Zip the shapefile
#

shutil.make_archive(ostem,'zip',ostem)

print(f'finished: ok to delete unzipped directory {ostem}')
