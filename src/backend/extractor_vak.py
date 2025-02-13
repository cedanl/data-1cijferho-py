import pandas as pd
import numpy as np
import re
from pathlib import Path
from typing import List

################################################################
#                            PATHS                           #
################################################################

# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "Bestandsbeschrijving_Vakkenbestanden.txt"
output_path = "bb_test.csv"

################################################################
#                          EXTRACT                          #
################################################################

# Import file
with open(file_path, encoding='latin1') as f:
    file_content = f.readlines()

# Check if file is empty
if len(file_content) == 0:
    raise Exception("File is empty or not properly read")

##--------------------------------
##  Identify Relevant Sections  
##--------------------------------
# Find start and end lines for both sections
start_line_df1 = next(i for i, line in enumerate(file_content) 
                    if "Decodeertabel vakcode" in line) + 3
end_line_df1 = next(i for i, line in enumerate(file_content) 
                    if "Vakgegevens" in line) - 1

start_line_df2 = next(i for i, line in enumerate(file_content) 
                    if "Vakgegevens" in line) + 3
end_line_df2 = len(file_content)  # Ga door tot het einde van het bestand

# Check if relevant sections are found
if not (start_line_df1 and end_line_df1 and start_line_df2):
    raise Exception("Start line markers not found in the file")

# Extract relevant sections
section_df1 = file_content[start_line_df1:end_line_df1]
section_df2 = file_content[start_line_df2:end_line_df2]

# Function to process a section of the file
# Input: List of strings
# Output: DataFrame
def process_section(section: List[str]) -> pd.DataFrame:
    data_list = []
    line_counter = 0
    
    for line in section:
        line_counter += 1
        
        if len(line.strip()) == 0:
            continue
            
        parts = [part for part in re.split(r'\s{2,}', line.strip()) if part]
        
        if len(parts) >= 3:
            data_list.append({
                'ID': line_counter,
                'Naam': parts[0],
                'Start_Positie': int(parts[1]),
                'Aantal_Posities': int(parts[2])
            })
    
    df = pd.DataFrame(data_list)
    
    # Voeg 'V' toe aan ID
    if not df.empty:
        df['ID'] = df['ID'].apply(lambda x: f"V{x}")
    
    # Sorteer op Start_Positie
    df = df.sort_values('Start_Positie')
    
    return df

# Process both sections
df1 = process_section(section_df1)
df2 = process_section(section_df2)

# Print resultaten
print("DataFrame 1 (Decodeertabel vakcode):")
print(df1)
print("\nDataFrame 2 (Vakgegevens):")
print(df2)

# Exporteer naar CSV
df1.to_csv(f"{output_path}_df1.csv", index=False)
df2.to_csv(f"{output_path}_df2.csv", index=False)