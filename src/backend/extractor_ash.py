################################################################
#                       COMPUTER MAGIC                          
################################################################
def display_table_section(text):
    """
    Extract and display the table section from the file description 
    until reaching an empty line.
    
    Args:
        text (str): The text containing the table
    """
    # Find the start of the table
    table_start = text.find("Startpositie  Aantal posities")
    if table_start == -1:
        print("Table not found")
        return
    
    # Get lines starting from the table header
    lines = text[table_start:].split('\n')
    
    # Print lines until we hit an empty line
    table_section = []
    for line in lines:
        if not line.strip():
            break
        table_section.append(line)
    
    # Print the table section
    print('\n'.join(table_section))

def extract_table_sections(text):
    """
    Identifies and extracts table sections containing 'Startpositie' and 'Aantal posities' columns,
    including only the title line with '===' above it.
    
    Args:
        text (str): The input text to search for table sections
        
    Returns:
        list: List of extracted table sections as strings
    """
    import re
    
    # Split the text into lines for easier processing
    lines = text.split('\n')
    table_sections = []
    
    # Look for the table header pattern
    header_pattern = re.compile(r'.*[Ss]tart[_ ]?[Pp]ositie.*[Aa]antal[_ ]?[Pp]osities.*')
    equal_sign_pattern = re.compile(r'^=+$')
    
    # Find table headers first
    table_start_indices = []
    for i, line in enumerate(lines):
        if header_pattern.match(line):
            table_start_indices.append(i)
    
    # Process each table
    for i, start_index in enumerate(table_start_indices):
        # Look for title with equal signs above the table
        title_line = None
        equal_line = None
        
        for j in range(start_index-1, max(0, start_index-20), -1):
            if equal_sign_pattern.match(lines[j].strip()):
                equal_line = j
                if j > 0:  # Make sure we have a line above
                    title_line = j-1
                break
        
        # Determine where this table ends
        if i < len(table_start_indices) - 1:
            # End at the start of the next table
            section_end = table_start_indices[i+1]
        else:
            # For the last table, find where it naturally ends
            section_end = len(lines)
            found_end = False
            for j in range(start_index+3, min(len(lines), start_index+30)):
                if not lines[j].strip() and j > start_index+3:
                    # Empty line after some content indicates end of table
                    section_end = j
                    found_end = True
                    break
            
            # If no natural end found, take a reasonable amount of lines
            if not found_end:
                section_end = min(len(lines), start_index+20)
        
        # Extract the table section including just the title and equal signs
        if title_line is not None and equal_line is not None:
            # Include the title line, equal line, and the table content
            section_lines = [lines[title_line], lines[equal_line]] + lines[start_index:section_end]
        else:
            # Just the table content if no title/equal sign found
            section_lines = lines[start_index:section_end]
            
        table_section = '\n'.join(section_lines)
        table_sections.append(table_section)
    
    return table_sections

# Example usage:
# with open('your_file.txt', 'r', encoding='utf-8') as file:
#     content = file.read()
#     tables = extract_table_sections(content)
#     for table in tables:
#         print(table)
#         print("\n" + "*"*50 + "\n")


path_1cho = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.txt"
path_croho = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Croho.txt"
path_croho_vest= "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Croho_vest.txt"
path_dec = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Dec-bestanden.txt"
path_vakkenbestand = "C:/Users/asewnandan/De Haagse Hogeschool/Fileserver Studiedata_groups - General/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_Vakkenbestanden.txt"

display_table_section(path_1cho)

with open(path_1cho, 'r', encoding='latin-1') as file:
     content = file.read()
     tables = extract_table_sections(content)
     for table in tables:
         print(table)
         print("\n" + "*"*50 + "\n")

with open(path_croho, 'r', encoding='latin-1') as file:
     content = file.read()
     tables = extract_table_sections(content)
     for table in tables:
         print(table)
         print("\n" + "*"*50 + "\n")

with open(path_croho_vest, 'r', encoding='latin-1') as file:
     content = file.read()
     tables = extract_table_sections(content)
     for table in tables:
         print(table)
         print("\n" + "*"*50 + "\n")

with open(path_dec, 'r', encoding='latin-1') as file:
     content = file.read()
     tables = extract_table_sections(content)
     for table in tables:
         print(table)
         print("\n" + "*"*50 + "\n")

with open(path_vakkenbestand, 'r', encoding='latin-1') as file:
     content = file.read()
     tables = extract_table_sections(content)
     for table in tables:
         print(table)
         print("\n" + "*"*50 + "\n")

