# Read mapping file using polars
import polars as pl
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn
from rich.pretty import pprint as rprint

################################################################
#                            PATHS                           
################################################################
# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "~/data/01-raw/DUO/1CHO/2025/EV27UM25.021"
mapping_path = "~/data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.csv"
output_path = "~/data/01-raw/DUO/1CHO/2025/EV27UM26.csv"

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


# Convert the file
converter(file_path, output_path, mapping_path)