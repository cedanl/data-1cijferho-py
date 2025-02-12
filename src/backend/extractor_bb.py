import pandas as pd
import numpy as np
import re
from pathlib import Path

################################################################
#                            PATHS                           
################################################################

# YOU CAN EDIT PATH BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "~/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.txt"

################################################################
#                          EXTRACT                          
################################################################

# Import file
with open(file_path, encoding='latin1') as f:
    file_content = f.readlines()

# Check if file is empty
if len(file_content) == 0:
    raise Exception("File is empty or not properly read")

##--------------------------------
##  Identify Relevant Section  
##--------------------------------
# Find start and end lines
start_line = next(i for i, line in enumerate(file_content) 
                 if "Lay-out bestand" in line) + 3  # CAN BE CHANGED
end_line = next(i for i, line in enumerate(file_content) 
                if "Vanwege de AVG" in line) - 1    # CAN BE CHANGED

# Check if relevant section is found
if not start_line or not end_line:
    raise Exception("Start or end line markers not found in the file")

# Extract relevant section
relevant_section = file_content[start_line:end_line]

##--------------------------
##  Extract Data Relevant Section
##--------------------------
data_list = []
skipped_data_list = []
line_counter = 0

# Process all relevant columns
for line in relevant_section:
    line_counter += 1
    
    if len(line.strip()) == 0:
        continue
    
    parts = [part for part in re.split(r'\s{2,}', line.strip()) if part]
    
    if len(parts) >= 3:
        data_list.append({
            'ID': line_counter,
            'Naam': parts[0],
            'Start_Positie': parts[1],
            'Aantal_Posities': parts[2]
        })
    else:
        skipped_data_list.append({
            'ID': line_counter,
            'Line': line.strip()
        })

# Convert lists to DataFrames
data = pd.DataFrame(data_list)

if skipped_data_list:
    skipped_data = pd.DataFrame(skipped_data_list)
else:
    print("No lines were skipped.")

##--------------------------
##  Extract Data skipped_data 
##--------------------------
if 'skipped_data' in locals() and not skipped_data.empty:
    skipped_data['Naam'] = skipped_data['Line'].str.extract(r'(.*?)(?=\s\d{3}\s{2,}\d)')
    skipped_data['Start_Positie'] = skipped_data['Line'].str.extract(r'(\d{3})(?=\s{2,}\d)')
    skipped_data['Aantal_Posities'] = skipped_data['Line'].str.extract(r'(\d+)$')
    
    # Delete Line column
    skipped_data = skipped_data.drop('Line', axis=1)

##--------------------------
##  Merge data + skipped_data DataFrames + misc.
##--------------------------
# Merge skipped_data with data
if 'skipped_data' in locals():
    data = pd.concat([data, skipped_data], ignore_index=True)

# Sort the merged dataset by ID
data = data.sort_values('ID')

##---------------------
##  Add AVG Column  
##---------------------
# Add AVG column based on (*)
data['AVG'] = data['Aantal_Posities'].str.contains(r'\*', regex=True)
data['Aantal_Posities'] = data['Aantal_Posities'].str.replace(r'[\*\(\)]', '', regex=True)

##---------------------
## Set Types
##---------------------
data['Start_Positie'] = pd.to_numeric(data['Start_Positie'])
data['Aantal_Posities'] = pd.to_numeric(data['Aantal_Posities'])

##---------------------
## ! Duplicate Check
##---------------------
duplicate_rows = data[data['Naam'].duplicated(keep=False)]

##---------------------
## ! Sum Check
##---------------------
sum_aantalposities = data['Aantal_Posities'].sum()
last_row_values = data['Start_Positie'].iloc[-1] + data['Aantal_Posities'].iloc[-1] - 1  # -1 because data starts at 1

is_equal = sum_aantalposities == last_row_values
print(f"Sum of Aantal_Posities: {sum_aantalposities}")
print(f"Last row value: {last_row_values}")
print(f"Values are equal: {is_equal}")

##---------------------
## Add V to ID
##---------------------
data['ID'] = 'V' + data['ID'].astype(str)

##---------------------
## PRINT CHECK
##---------------------
print(data)