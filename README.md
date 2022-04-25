## North Carolina Residential Solar Analysis 

# Background and Purpose 

This repository contains scripts that conduct a county-level analysis to predict potential residential solar generation capacity for all 100 counties in North Carolina. Using parcel data, building footprints, and census variables the analysis estimates the potential volume of residential solar feasible for installation in each county. The scripts also include a detailed analysis of potential residential solar generation capacity in North Carolina’s environmental justice communities. The analysis geographically identifies environmental justice communities according to parameters regarding race and median income and creates geopackage files that the user can use to heat map potential solar kilowatt capacity and environmental justice community locations. 

The results of this analysis are intended to support the clean energy transition and promote energy justice through increased residential solar installations in North Carolina’s environmental justice communities. 

# Modifying the county.json file 
1.	Open the nc_counties.csv file saved in the repository and locate the county of interest. 
2.	Open the county.json file saved in the repository and update the county name, geoid, and FIPS code. 

# External Data 
**Parcels:** 
1.	Go to https://www.nconemap.gov/pages/parcels and download parcel data for the county of interest.
**Building Footprints:** 
1.	Go to the Microsoft Building Footprint GitHub site (https://github.com/Microsoft/USBuildingFootprints) and download the building footprint file for North Carolina.
**Census Blocks:**
1.	Go to the Census TIGER/Line Files page (https://www.census.gov/geographies/mapping-files/time-series/geo/tiger-line-file.html) and download the 2019 Census block and block group files for North Carolina.  

# Scripts 
**00_NC_analyze.py**
Reads and analyzes state-level Census block group data regarding race and median income and defines the parameters for potential environmental justice communities in a json file (NC_info.json) used in later scripts to identify potential environmental justice communities.
#
**01_census_blocks.py**
Reads the North Carolina Census block TIGER/Line file, retrieves population data for each block via a Census API call, filters the blocks to the county of interest, only keeps blocks where people live (population > 0), and writes out a county specific block file.
#
**02_merge_bfp_parcel.py**
Reads the Microsoft building file, and the county specific parcel file, reprojects both files to epsg 32617, converts the building footprint to centroids, computes each building footprint’s area and includes this as an attribute, spatially joins the buildings footprints and parcels and writes out the results in a geopackage.
#
**03_largest_bfp.py**
Reads the merged building footprint and parcel file from the previous script, filters the buildings based on size, only keeps the largest building footprint on each parcel, and writes out a geopackage.
#
**04_merge_bfp_blocks.py**
Reads in the largest building file from the previous script and the county block output file from the 01_census_blocks.py script, spatially joins the two files, and writes out a geopackage.
#
**05_block_houses_bgs.py**
Reads in the merged building footprint and block file from the previous script, the county block output file from the 01_cenuss_blocks.py script, and the North Carolina Census block group TIGER/Line file. 

Filters the buildings to only keep those that are less than 500 m2, calculates the usable area and potential solar capacity (kW) of each roof, groups the blocks by block group, merges the block data onto the block geography, and writes out a geopackage that includes the number of buildings, the usable area, and the estimated kW capacity by block and block group. 
#
**06_census_acs.py**
Retrieves data regarding race, median income in the past 12 months, and year structure built for county block groups and writes out the results in a csv. 
#
**07_analyze.py**
Reads in the csv file from the previous script and the output file from the 05_block_houses_bgs.py script. 

Calculates the percent of homes in each block group built during or after 1950 and applies this proportion to the usable area estimate. 

Calculates the percent of people of color in each block group and assigns the environmental justice community flag “R” to block groups that are above the threshold identified in 00_NC_analyze.py script and corresponding NC_info.json file.

Assigns the environmental justice community flag “E” to block groups that are below the median income threshold identified in 00_NC_analyze.py script and corresponding NC_info.json file.

Calculates the mean kW per house by block group. 

Writes out the results in a geopackage. 
