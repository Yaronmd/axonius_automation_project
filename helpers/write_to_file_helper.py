import logging
import os
from datetime import datetime
def log_results_to_temp_folder(file_name:str,**kwargs):
    """Log the highest rated and cheapest result to a custom log file in the 'temp' folder."""
    
    # validate 'temp' directory exists
    temp_folder = 'temp'
    if not os.path.exists(temp_folder):
        os.makedirs(temp_folder)  # Create 'temp' directory if it doesn't exist
    
    # Path for the log file inside the 'temp' folder
    log_file_path = os.path.join(temp_folder, f'{file_name}.log')

    with open(log_file_path, 'a') as log_file:
        for key, value in kwargs.items():
            if value:
                log_file.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}: {key.replace('_', ' ').capitalize()}: {value}\n")
        log_file.write(f"-------------------\n")
