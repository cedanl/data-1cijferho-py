
# Nmap
# Numpy
# Multiprocessing
import polars as pl
from pathlib import Path
import mmap
import os
import time

################################################################
#                            PATHS                           
################################################################
# YOU CAN EDIT PATHS BELOW - PLEASE DO NOT ADJUST ANY OTHER FUNCTIONS
file_path = "~/data/01-raw/DUO/1CHO/2025/EV27UM25.021"
path_mapping_1cho = "~/data/01-raw/DUO/1CHO/2025/bb_test.csv"
csv_cho1 = "~/data/01-raw/DUO/1CHO/2025/EV27UM25.csv"

################################################################
#                       COMPUTER MAGIC                          
################################################################
def convert_fwf_to_csv(input_file: str, output_file: str, widths: list, encoding: str = 'latin1', 
                       chunk_size: int = 1_000_000) -> None:
    """
    Convert fixed-width file to CSV using memory mapping for maximum performance.
    Uses a pipe (|) as delimiter for faster processing.
    """
    # Calculate position markers for the fixed-width columns
    positions = [(sum(widths[:i]), sum(widths[:i+1])) for i in range(len(widths))]
    
    # Open files in binary mode for maximum performance
    with open(input_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        # Memory map the input file for faster reading
        mm = mmap.mmap(f_in.fileno(), 0, access=mmap.ACCESS_READ)
        
        # Process file in chunks for memory efficiency
        offset = 0
        line_length = sum(widths) + 1  # +1 for newline character
        
        while True:
            # Read a chunk of the file
            chunk = mm.read(chunk_size * line_length)
            if not chunk:
                break
                
            # Find the last complete line in the chunk
            last_newline = chunk.rfind(b'\n')
            if last_newline != -1:
                process_chunk = chunk[:last_newline]
                mm.seek(offset + last_newline + 1)
            else:
                process_chunk = chunk
                
            # Split into lines and process
            lines = process_chunk.split(b'\n')
            
            # Process each line
            output_lines = []
            for line in lines:
                if not line:  # Skip empty lines
                    continue
                    
                # Extract fields based on positions
                fields = [line[start:end].decode(encoding).strip() for start, end in positions]
                output_line = '|'.join(fields).encode(encoding) + b'\n'
                output_lines.append(output_line)
            
            # Write processed lines
            f_out.writelines(output_lines)
            
            offset = mm.tell()
        
        mm.close()

start_time = time.time()

# Read mapping file using polars
mapping_df = pl.read_csv(path_mapping_1cho)

# Adjust mapping as per original R code
mapping_df = mapping_df.with_columns(
    pl.when(pl.col("Aantal_Posities").arg_min() == pl.lit(0))
    .then(pl.lit(10))
    .otherwise(pl.col("Aantal_Posities"))
    .alias("Aantal_Posities")
)

# Remove last two records (equivalent to R code)
mapping_df = mapping_df.slice(0, len(mapping_df) - 2)

# Get widths for processing
widths = mapping_df["Aantal_Posities"].to_list()

# Convert the file
convert_fwf_to_csv(file_path, csv_cho1, widths, encoding='latin1')

end_time = time.time()
print(f"Duration: {end_time - start_time:.2f} seconds")
