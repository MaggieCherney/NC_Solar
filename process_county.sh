#! /bin/zsh
#touch county/full_${1}.csv

python 01_county_select.py    2>&1
python 02a_census_blocks.py   2>&1
python 03_merge_bfp_parcel.py 2>&1
python 04_largest_bfp.py      2>&1
python 05_merge_bfp_blocks.py 2>&1
python 06_block_houses_bgs.py 2>&1
python 08_analyze.py          2>&1

#mv bfp_${1}.gpkg temp/ 
#mv blocks_${1}.gpkg temp/ 
rm -f bfp_${1}.gpkg blocks_${1}.gpkg
rm -f houses_by_block_${1}.gpkg largest_buildings_${1}.gpkg 
rm -f merged_bfp_blocks_${1}.gpkg merged_bfp_parcels_${1}.gpkg
# remove all of the intermediate gpkg
# run the script on one new file 