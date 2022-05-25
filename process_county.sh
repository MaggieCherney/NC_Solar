#! /bin/zsh
#touch county/full_${1}.csv

python 01_county_select.py
python 02_census_blocks.py
python 03_merge_bfp_parcel.py
python 04_largest_bfp.py
python 05_merge_bfp_blocks.py
python 06_block_houses_bgs.py
python 07_census_acs.py
python 08_analyze.py

#mv bfp_${1}.gpkg temp/ 
#mv blocks_${1}.gpkg temp/ 
rm -f bfp_${1}.gpkg blocks_${1}.gpkg census-acs-bgs-${1}.csv 
rm -f houses_by_block_${1}.gpkg largest_buildings_${1}.gpkg 
rm -f merged_bfp_blocks_${1}.gpkg merged_bfp_parcels_${1}.gpkg
# remove all of the intermediate gpkg
# run the script on one new file 