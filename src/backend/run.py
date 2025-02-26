from extractor import find_tables_from_file
import os

# Import File Overview

# Import Folder 

# ---

# Execute extractor() 
# --- TEMPORARY --- 
# Finds all tables in a given directory and saves them to a JSON file
def find_and_process_files(root_path):
    for root, dirs, files in os.walk(root_path):
        for file in files:
            if "Bestandsbeschrijving" in file and file.endswith(".txt"):
                full_path = os.path.join(root, file)
                find_tables_from_file(full_path)

root_directory = "data/01-raw/DUO/1CHO/2025/"
find_and_process_files(root_directory)

# Execute converter()

# Execute decoder()

# ---

# Buy Porsche
