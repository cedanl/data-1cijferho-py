from extractor import find_tables_from_file

# Import File Overview

# Import Folder 

# ---

# Execute extractor()
path_1cho = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.txt"
path_croho = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Croho.txt"
path_croho_vest= "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Croho_vest.txt"
path_dec = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Dec-bestanden.txt"
path_vakkenbestand = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Vakkenbestanden.txt"


file_paths = [path_1cho,path_croho, path_croho_vest, path_dec, path_vakkenbestand]
for path in file_paths:
    find_tables_from_file(path)

# Execute converter()

# Execute decoder()

# ---

# Buy Porsche
