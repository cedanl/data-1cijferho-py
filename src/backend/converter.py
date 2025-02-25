import multiprocessing as mp
import os
from functools import partial
import polars as pl
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn, TimeElapsedColumn


################################################################
#                            PATHS                           
################################################################
# YOU CAN EDIT PATHS BELOW IN THE MAIN SECTION- PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS

################################################################
#                       COMPUTER MAGIC                          
################################################################

def process_chunk(chunk_data):
    """
    Process a chunk of lines and return the converted output
    """
    positions, chunk = chunk_data
    output_lines = []
    for line in chunk:
        if isinstance(line, bytes):
            line = line.decode('latin1')  # Adjust encoding as needed
        if line.strip():  # Skip empty lines
            fields = [line[start:end].strip() for start, end in positions]
            output_lines.append('|'.join(fields))
    return output_lines

def converter(input_file, output_file, mapping_path, encoding='latin1'):
    """
    Convert fixed-width file to CSV using multiprocessing for better performance
    """
    # Load mapping
    mapping_df = pl.read_csv(mapping_path)
    widths = mapping_df["Aantal_Posities"].to_list()
    column_names = mapping_df["Naam"].to_list()
    
    # Calculate positions for each field
    positions = [(sum(widths[:i]), sum(widths[:i+1])) for i in range(len(widths))]
    
    # Count total lines
    with open(input_file, 'rb') as f:
        total_lines = sum(1 for _ in f.readlines())
    
    console = Console()
    
    # Write header first
    with open(output_file, 'w', encoding=encoding, newline='') as f_out:
        f_out.write('|'.join(column_names) + '\n')
    
    # Read the entire file into memory (if it's not too large)
    with open(input_file, 'r', encoding=encoding) as f_in:
        all_lines = f_in.readlines()
    
    # Set up multiprocessing (safely)
    with Progress(
        SpinnerColumn(),
        TextColumn("[cyan]Converting..."),
        BarColumn(),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TimeElapsedColumn(),
        console=console,
    ) as progress:
        task = progress.add_task("", total=total_lines)
        
        try:
            # Determine chunk size and number of processes
            num_processes = max(1, mp.cpu_count() - 1)  # Leave one core free
            chunk_size = max(1, len(all_lines) // (num_processes * 4))  # Create 4x as many chunks as processes
            
            # Split data into chunks
            chunks = [all_lines[i:i + chunk_size] for i in range(0, len(all_lines), chunk_size)]
            chunk_data = [(positions, chunk) for chunk in chunks]
            
            # Process in parallel
            with mp.Pool(processes=num_processes) as pool:
                results_iter = pool.imap_unordered(process_chunk, chunk_data)
                
                # Write results as they come in
                lines_processed = 0
                with open(output_file, 'a', encoding=encoding, newline='') as f_out:
                    for result in results_iter:
                        if result:
                            f_out.write('\n'.join(result) + '\n')
                        lines_processed += len(result) if result else 0
                        progress.update(task, completed=min(lines_processed, total_lines))
            
        except Exception as e:
            console.print(f"[red]Error during conversion: {str(e)}")
            raise
    
    console.print("[green]Conversion completed successfully! ✨")

################################################################
#                            MAIN                           
################################################################
# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS

# Only run this section if the script is being run directly
# Run with 'uv run ./src/backend/converter.py'
if __name__ == "__main__":
    # You can define your variables here if needed:
    file_path = "-data/01-raw/DUO/1CHO/2025/EV27UM25.021"
    mapping_path = "-data/01-raw/DUO/1CHO/2025/Bestandsbeschrijving_1cyferho_2024_v1.1.csv"
    output_path = "-data/01-raw/DUO/1CHO/2025/EV27UM26.csv"
    converter(file_path, output_path, mapping_path)

