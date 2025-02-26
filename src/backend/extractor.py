import os
import json
import re

def find_tables_from_file(file_path):
    # Read the file content
    try:
        with open(file_path, 'r', encoding='latin-1') as file:
            text = file.read()
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return
    except Exception as e:
        print(f"Error reading file: {e}")
        return
    
    # Ensure data directory exists
    data_dir = os.path.join(os.getcwd(), 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    # Get the base filename without extension
    base_filename = os.path.splitext(os.path.basename(file_path))[0]
    
    # Process the text to find tables
    lines = text.split('\n')
    found = False
    table_title = ""
    table_content = []
    tables_found = 0
    all_tables = []
    
    for i, line in enumerate(lines):
        # Check for table header
        if "startpositie" in line.lower() and not found:
            found = True
            tables_found += 1
            table_content = [line]  # Start collecting table content
            
            # Look backwards to find the title
            title_found = False
            for j in range(i-1, max(0, i-10), -1):  # Look at up to 10 lines above
                if lines[j].strip().startswith('=='):
                    # Title is the line above the === line
                    if j > 0 and lines[j-1].strip():
                        table_title = lines[j-1].strip()
                        title_found = True
                        break
            
            if not title_found:
                table_title = f"untitled_table_{tables_found}"
                
            print(f"\nFound Table {tables_found}: {table_title}")
        
        # Collect table content
        elif found:
            if not line.strip():
                found = False
                
                # Add the table to our collection
                table_data = {
                    "table_number": tables_found,
                    "table_title": table_title,
                    "content": table_content
                }
                
                all_tables.append(table_data)
                table_content = []
                continue
            
            print(line)
            table_content.append(line)
    
    # Check if the last table extends to the end of the file
    if found and table_content:
        table_data = {
            "table_number": tables_found,
            "table_title": table_title,
            "content": table_content
        }
        
        all_tables.append(table_data)
    
    # Save all tables to a single JSON file
    if all_tables:
        file_data = {
            "filename": base_filename,
            "tables": all_tables
        }
        
        json_filename = f"{base_filename}.json"
        json_path = os.path.join(data_dir, json_filename)
        
        with open(json_path, 'w', encoding='latin-1') as json_file:
            json.dump(file_data, json_file, indent=2, ensure_ascii=False)
        
        print(f"\nSaved all {tables_found} tables to {json_path}")
    else:
        print(f"\nNo tables found in {file_path}")
