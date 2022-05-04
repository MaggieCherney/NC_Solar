# North Carolina Residential Solar Analysis 

## Background and Purpose 

This repository contains scripts that conduct a county-level analysis to predict potential residential solar generation capacity for all 100 counties in North Carolina. Using parcel data, building footprints, and census variables the analysis estimates the potential volume of residential solar feasible for installation in each county. The scripts also include a detailed analysis of potential residential solar generation capacity in North Carolina’s environmental justice communities. The analysis geographically identifies environmental justice communities according to parameters regarding race and median income and creates geopackage files that the user can use to heat map potential solar kilowatt capacity and environmental justice community locations. 

The results of this analysis are intended to support the clean energy transition and promote energy justice through increased residential solar installations in North Carolina’s environmental justice communities. 

## External Data 
**Parcels:** Go to https://www.nconemap.gov/pages/parcels and download parcel data for the county of interest.(*needs to be downloaded once per county*)

**Building Footprints:** Go to the Microsoft Building Footprint GitHub site (https://github.com/Microsoft/USBuildingFootprints) and download the building footprint file for North Carolina.(*only needs to be downloaded once for the state*)

**Census Counties, Blocks Groups, and Blocks:** Go to the Census TIGER/Line Files page (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) and download the US 2019 Census county TIGER/Line File and the North Carolina 2019 Census block groups and block TIGER/Line Files. (*only need to be downloaded once for the state*)  

## Selecting the county 
1.	Open the nc_counties.csv file saved in the repository and locate the county of interest. 
2.	Open the county.json file saved in the repository and update the county name and geoid.

## Scripts 
**00_NC_analyze.py** (*only needs to be run once for the state*)
Reads and analyzes an existing csv file in the repository that contains North Carolina's Census block group data regarding race and median income. 

Defines the parameters for potential environmental justice communities in a json file (NC_info.json) used in later scripts to identify potential environmental justice communities.
#
**00_state_shapefile.py** (*only needs to be run once for the state*)
Reads in the North Carolina Microsoft building footprint file and converts the geojson (.geojson) file to a shape file (.shp).
#
**01_county_select.py** (*needs to be run once per county*)
Reads in the North Carolina Microsoft building footprint shape file and the Census county file, selects the building footprints for the county of interest, and writes out the results as a geopackage.  
#
**02_census_blocks.py** (*needs to be run once per county*)
Reads the North Carolina Census block TIGER/Line file, retrieves population data for each block via a Census API call, filters the blocks to the county of interest, only keeps blocks where people live (population > 0), and writes out a county specific block file.
#
**03_merge_bfp_parcel.py** (*needs to be run once per county*)
Reads the Microsoft building file, and the county specific parcel file, reprojects both files to epsg 32617, converts the building footprint to centroids, computes each building footprint’s area and includes this as an attribute, spatially joins the buildings footprints and parcels and writes out the results in a geopackage.
#
**04_largest_bfp.py** (*needs to be run once per county*)
Reads the merged building footprint and parcel file from the previous script, filters the buildings based on size, only keeps the largest building footprint on each parcel, and writes out a geopackage.
#
**05_merge_bfp_blocks.py** (*needs to be run once per county*)
Reads in the largest building file from the previous script and the county block output file from the 01_census_blocks.py script, spatially joins the two files, and writes out a geopackage.
#
**06_block_houses_bgs.py** (*needs to be run once per county*)
Reads in the merged building footprint and block file from the previous script, the county block output file from the 01_cenuss_blocks.py script, and the North Carolina Census block group TIGER/Line file. 

Filters the buildings to only keep those that are less than 500 m2, calculates the usable area and potential solar capacity (kW) of each roof, groups the blocks by block group, merges the block data onto the block geography, and writes out a geopackage that includes the number of buildings, the usable area, and the estimated kW capacity by block and block group. 
#
**07_census_acs.py** (*needs to be run once per county*)
Retrieves data regarding race, median income in the past 12 months, and year structure built for county block groups and writes out the results in a csv. 
#
**08_analyze.py** (*needs to be run once per county*)
Reads in the csv file from the previous script and the output file from the 05_block_houses_bgs.py script. 

Calculates the percent of homes in each block group built during or after 1950 and applies this proportion to the usable area estimate. 

Calculates the percent of people of color in each block group and assigns the environmental justice community flag “R” to block groups that are above the threshold identified in 00_NC_analyze.py script and corresponding NC_info.json file.

Assigns the environmental justice community flag “E” to block groups that are below the median income threshold identified in 00_NC_analyze.py script and corresponding NC_info.json file.

Calculates the mean kW per house by block group, groups the houses by the environmental justice indicators, calculates the proportion of kW capacity in environmental justice communities, and calculates the proportion of the population in environmental justice communities. 

Writes out the results in a geopackage and a csv. 
