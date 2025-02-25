import pandas as pd
import re
from typing import List, Dict, Optional


pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)

def extract_tables(file_path: str, encoding: str = 'latin-1') -> Dict[str, pd.DataFrame]:
    """
    Extract tables from a file with consistent formatting.
    
    Args:
        file_path: Path to the text file
        encoding: File encoding (default: 'latin-1')
        
    Returns:
        Dictionary of DataFrames with table names as keys
    """
    def read_file(file_path: str, encoding: str) -> List[str]:
        try:
            with open(file_path, 'r', encoding=encoding) as file:
                return file.readlines()
        except UnicodeDecodeError:
            raise Exception(f"Could not decode the file with encoding: {encoding}")

    def find_table_sections(lines: List[str]) -> List[Dict]:
        sections = []
        current_section = None
        for i, line in enumerate(lines):
            if line.strip().endswith('.asc') or line.strip().startswith("Dec"):
                if current_section:
                    current_section['end'] = i
                    sections.append(current_section)
                current_section = {'name': line.strip(), 'start': i + 1}
        if current_section:
            current_section['end'] = len(lines)
            sections.append(current_section)
        return sections

    def process_section(section: Dict, lines: List[str]) -> pd.DataFrame:
        data = []
        for line in lines[section['start']:section['end']]:
            parts = [part for part in re.split(r'\s{2,}', line.strip()) if part]
            if len(parts) >= 3:
                try:
                    data.append({
                        'Naam': parts[0],
                        'Start_Positie': int(parts[-2]),
                        'Aantal_Posities': int(parts[-1].split()[0]),
                        'Extra': ' '.join(parts[-1].split()[1:]) if len(parts[-1].split()) > 1 else ''
                    })
                except ValueError:
                    continue  # Skip lines that can't be parsed
        return pd.DataFrame(data)

    lines = read_file(file_path, encoding)
    sections = find_table_sections(lines)
    tables = {}

    for section in sections:
        df = process_section(section, lines)
        if not df.empty:
            table_name = section['name'].replace('=', '').replace(' ', '_').strip()
            tables[table_name] = df

    return tables

# Usage
## the space is missing between the columns
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_1cyferho_2024_v1.1.txt"
file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_Vakkenbestanden.txt"

# works:
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_Dec-bestanden.txt"


## issues as not following template
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_Croho.txt"
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_hoacth_vest_2024_v1.0.txt"
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_hoacth_2024_v1.0.txt"
# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_Croho_vest.txt"

## fake data

# file_path = "/referentietabellen en documentatie/Bestandsbeschrijving_Numerus_fixus_2000-[JJJJ].txt"

tables = extract_tables(file_path)

# Print table names and their dimensions
for table_name, df in tables.items():
    print(f"\n{'-'*50}")
    print(f"Table: {table_name}")
    print(f"Dimensions: {df.shape}")
    print(f"{'-'*50}")
    print(df.head(100))
    print(f"{'-'*50}\n")
