#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 26 15:53:49 2022

@author: maggiecherney
"""

import requests
import pandas as pd
import json

print("started 02a_census_blocks.py")

specs = json.load( open('county.json') )
county_code = specs['geoid']

tl_2019_block_file = "tl_2019_37_tabblock10.zip"

output_file = f'census_blocks_{county_code}.csv'

api = "https://api.census.gov/data/2010/dec/sf1"

for_clause = 'block:*'        
in_clause = f"county:{county_code[2:]} state:37"

key_value = "5e68fcb5c9823ef307b5126995727b3ae470dc0d"

payload = {'get':'P003001',
           'for':for_clause,
           'in':in_clause,
           'key':key_value}

response = requests.get(api,payload,timeout=1)
response.raise_for_status()

#%%

# use an if statement to test whether response.status_code is equal to 200
# print a message if it is successful 
# use an else statement to print the response.text and add assert False 
# to stop the script if the statement is reached 

if response.status_code == 200:
    print('\nrequest successful')
else:
    print(response.status_code) 
    print(response.text)
    assert False

# parse the JSON returned by the Census server and return a list of rows 

row_list = response.json()

#%%

# set the column names to the first row of row_list

colnames = row_list[0]

# set the data rows to the remaining rows of row_list 

datarows = row_list[1:]

# convert the data into a Pandas dataframe 

blocks = pd.DataFrame(columns=colnames,data=datarows)

# use a dictionary called new_names to rename columns 

new_names = {"P003001":"pop"}

# convert the data into a Pandas dataframe 

blocks = blocks.rename(columns=new_names)

st = blocks['state']
co = blocks['county']
tr = blocks['tract']
bk = blocks['block']
        
blocks['geoid'] = st+co+tr+bk

blocks.set_index('geoid',inplace=True)

blocks.to_csv(output_file)