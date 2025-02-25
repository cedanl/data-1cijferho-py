################################################################
#                           EXTRACTOR                           
################################################################
def extract_tables(file_path):
    """
    Extract tables from a file with consistent formatting.
    Handles different file encodings.
    
    Args:
        file_path: Path to the text file
        
    Returns:
        Dictionary of DataFrames with table names prefixed with "bb_"
    """
    import pandas as pd
    
    # Try different encodings
    encodings = ['utf-8', 'latin-1', 'cp1252', 'iso-8859-1']
    
    for encoding in encodings:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                lines = file.readlines()
            break  # If successful, exit the loop
        except UnicodeDecodeError:
            if encoding == encodings[-1]:  # If this was the last encoding to try
                raise Exception(f"Could not decode the file with any of these encodings: {encodings}")
            continue
    
    tables = {}
    i = 0
    
    while i < len(lines):
        line = lines[i].strip()
        
        # Check if this is a table title (ends with .asc and followed by equals signs)
        if line.endswith('.asc') and i + 1 < len(lines) and '===' in lines[i + 1]:
            table_name = line
            var_name = f"bb_{table_name}"
            
            # Skip title and equals line
            i += 2
            
            # Skip blank lines before header
            while i < len(lines) and not lines[i].strip():
                i += 1
            
            # Skip the header line
            if i < len(lines) and "Startpositie" in lines[i] and "Aantal posities" in lines[i]:
                i += 1
            
            # Collect data rows
            data = []
            while i < len(lines) and lines[i].strip():
                line_text = lines[i].strip()
                parts = line_text.split()
                
                if len(parts) >= 2 and parts[-2].isdigit():
                    # Check if the length part is a digit
                    length_part = parts[-1]
                    if length_part.isdigit():
                        # Simple case: no extra info
                        field_name = ' '.join(parts[:-2])
                        start_pos = int(parts[-2])
                        length = int(length_part)
                        extra = ""
                    else:
                        # There's a digit followed by something
                        digit_part = ""
                        for char in length_part:
                            if char.isdigit():
                                digit_part += char
                            else:
                                break
                                
                        if digit_part:
                            # We found digits at the start
                            field_name = ' '.join(parts[:-2])
                            start_pos = int(parts[-2])
                            length = int(digit_part)
                            
                            # Get everything after the numbers in the line
                            pos_after_length = line_text.find(length_part) + len(digit_part)
                            extra = line_text[pos_after_length:].strip()
                        else:
                            # Skip this line if we can't parse it
                            i += 1
                            continue
                    
                    data.append({
                        'Naam': field_name,
                        'startpositie': start_pos,
                        'aantal_posities': length,
                        'extra': extra
                    })
                i += 1
            
            # Create DataFrame for this table
            if data:
                tables[var_name] = pd.DataFrame(data)
        else:
            i += 1
    
    return tables

# Now you can access each table by its variable name
# For example:
# Just print table names and their dimensions
# Assuming your tables are stored in a variable called 'tables'
for table_name, df in tables.items():
    print(f"\n{'-'*50}")
    print(f"Table: {table_name}")
    print(f"{'-'*50}")
    print(df)
    print(f"{'-'*50}\n")