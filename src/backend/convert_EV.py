import polars as pl
from pathlib import Path
import mmap
import os
import time
from rich.progress import Progress, SpinnerColumn, TimeElapsedColumn, BarColumn, TextColumn
from rich.console import Console
from rich import print as rprint

################################################################
#                            PATHS                           
################################################################
# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "/data/01-raw/DUO/1CHO/2025/EV27UM25.021"
path_mapping_1cho = "/data/01-raw/DUO/1CHO/2025/bb_test.csv"
csv_cho1 = "/data/01-raw/DUO/1CHO/2025/EV27UM25.csv"

################################################################
#                       COMPUTER MAGIC                          
################################################################

def convert_fwf_to_csv(input_file: str, output_file: str, widths: list, column_names: list, encoding: str = 'latin1'):
    """
    Convert fixed-width file to CSV using simple file reading for better progress tracking
    """
    # Calculate positions for each field
    positions = [(sum(widths[:i]), sum(widths[:i+1])) for i in range(len(widths))]
    
    # Count total lines for progress bar
    total_lines = sum(1 for _ in open(input_file, encoding=encoding))
    
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
        
        with open(input_file, 'r', encoding=encoding) as f_in, \
             open(output_file, 'w', encoding=encoding, newline='') as f_out:
            
            # Write header
            f_out.write('|'.join(column_names) + '\n')
            
            # Process lines
            for line in f_in:
                if line.strip():  # Skip empty lines
                    fields = [line[start:end].strip() for start, end in positions]
                    f_out.write('|'.join(fields) + '\n')
                progress.update(task, advance=1)

    rprint("[green]Conversion completed successfully! ✨")

start_time = time.time()

# Read mapping file using polars
mapping_df = pl.read_csv(path_mapping_1cho)
widths = mapping_df["Aantal_Posities"].to_list()
column_names = mapping_df["Naam"].to_list()

# Convert the file
convert_fwf_to_csv(file_path, csv_cho1, widths, column_names)

end_time = time.time()
rprint(f"[bold blue]Total Duration:[/bold blue] {end_time - start_time:.2f} seconds")