import polars as pl
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.pretty import pprint as rprint

################################################################
#                            PATHS                           
################################################################
# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "~data/01-raw/DUO/1CHO/2025/EV27UM25.021"
mapping_path = "~data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.csv"
output_path = "~data/01-raw/DUO/1CHO/2025/EV27UM26.csv"

################################################################
#                       COMPUTER MAGIC                          
################################################################

def converter(input_file: str, output_file: str, mapping_path: str, encoding: str = 'latin1'):
    """
    Convert fixed-width file to CSV using simple file reading for better progress tracking
    
    Parameters:
    -----------
    input_file : str
        Path to the fixed-width file
    output_file : str
        Path where the CSV file will be saved
    mapping_path : str
        Path to the mapping file containing column widths and names
    encoding : str, default 'latin1'
        Encoding of the input and output files
    """
    mapping_df = pl.read_csv(mapping_path)
    widths = mapping_df["Aantal_Posities"].to_list()
    column_names = mapping_df["Naam"].to_list()
    
    # Calculate positions for each field
    positions = [(sum(widths[:i]), sum(widths[:i+1])) for i in range(len(widths))]
    
    # Count total lines more efficiently
    with open(input_file, 'rb') as f:
        total_lines = sum(1 for _ in f.readlines())
    
    console = Console()
    
    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Converting..."),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("", total=total_lines)
        
        # Use chunking to process the file faster
        chunk_size = 10000  # Adjust based on memory availability
        
        with open(input_file, 'r', encoding=encoding) as f_in, \
             open(output_file, 'w', encoding=encoding, newline='') as f_out:
            
            # Write header
            f_out.write('|'.join(column_names) + '\n')
            
            # Process lines in chunks
            lines_processed = 0
            while True:
                lines = f_in.readlines(chunk_size)
                if not lines:
                    break
                
                # Process all lines in the chunk at once
                output_lines = []
                for line in lines:
                    if line.strip():  # Skip empty lines
                        fields = [line[start:end].strip() for start, end in positions]
                        output_lines.append('|'.join(fields))
                
                # Write all processed lines at once
                f_out.write('\n'.join(output_lines) + '\n')
                
                # Update progress
                lines_processed += len(lines)
                progress.update(task, completed=lines_processed)

    rprint("[green]Conversion completed successfully! ✨")


# Convert the file
converter(file_path, output_path, mapping_path)