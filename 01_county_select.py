"""
county_select.py
Oct 2021 PJW

Extract building footprints for a given county from the MS 
footprint file. Can read either the original zipped geojson files 
or zipped shapefiles built from them. The latter is much faster 
once the initial conversion is finished.
"""

import geopandas as gpd
import json
import sys

#
#  Where to find instructions on what to do:
#
#     shp_file = MS building file for the state
#
#     geoid    = desired county's 5-digit GEIOD
#     cfile    = Census county shapefile for the state
#

state = json.load( open('state.json') )
bfile = state['shp_file']

specs = json.load( open('county.json') )
geoid = specs['geoid']
cfile = specs['cfile']

#
#  What to name the output file
#

gfile = f"bfp_{geoid}.gpkg"

#
#  Read the county shapefile and filter it down to the county of 
#  interest
#

print( "reading the county shape file...", flush=True )
all_county = gpd.read_file( cfile )

this_county = all_county.query( f"GEOID == '{geoid}'" )
this_county = this_county.to_crs(epsg=4326)

n = len(this_county)
if n != 1:
    sys.exit( f"wrong number of counties found: {n}" )
    
print( f"county {geoid} is", this_county.iloc[0]['NAME'] )

this_county = this_county[['GEOID','geometry']]

#
#  Read the footprint file. Use the bounding box for the county 
#  to restict the footprints being loaded
#

print( "\nreading the footprint file...", flush=True )
build = gpd.read_file( bfile, bbox=this_county )
print( "buildings found in bounding box:", len(build) )

#
#  Now select the footprints that lie wholly within the county 
#  boundary
#

print( "\ntrimming to buildings within the county boundary...", flush=True)
build = gpd.sjoin(build, this_county, how='inner', predicate='within' )
build.drop(columns="index_right",inplace=True)
print( "buildings found within county boundary:", len(build) )

#
#  Write both the county and buildings to the output file.
#

print( f"\nwriting layers to {gfile}:" )

print( f"   county boundary, {len(this_county)} feature...", flush=True )
this_county.to_file( gfile, layer="county", driver="GPKG", index=False )

print( f"   building footprints, {len(build)} features...", flush=True )
build.to_file( gfile, layer="buildings", driver="GPKG", index=False )
