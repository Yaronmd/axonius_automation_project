import logging
import os
from datetime import datetime
def log_results_to_temp_folder(file_name:str,**kwargs):
    """Log the highest rated and cheapest result to a custom log file in the 'temp' folder."""
    
    # Step 1: Ensure the 'temp' directory exists
    temp_folder = 'temp'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)  # Create 'temp' directory if it doesn't exist
    
    # Path for the log file inside the 'temp' folder
    log_file_path = os.path.join(temp_folder, f'{file_name}.log')

    # Step 2: Open the file in append mode ('a') so we don't overwrite existing content
    with open(log_file_path, 'a') as log_file:
        # Write the log entry manually
        for key, value in kwargs.items():
            if value:  # If the value is not None or an empty string
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {key.replace('_', ' ').capitalize()}: {value}\n")
        log_file.write(f"-------------------\n")
