import pandas as pd
import numpy as np
import time
from datetime import datetime
import os
import yaml

import json
import classification as cl

CONFIG = None


def load_config(file_path="config.yaml"):
    """
    Load configuration from a YAML file into a global variable.
    """
    global CONFIG
    if CONFIG is None:  # Load only once
        with open(file_path, "r") as file:
            CONFIG = yaml.safe_load(file)

def get_config():
    """
    Access the loaded configuration.
    """
    global CONFIG
    if CONFIG is None:
        raise RuntimeError("Configuration has not been loaded. Call `load_config()` first.")
    return CONFIG


def create_prompt(instruction,taxonomy):
    # 1. Read the contents of each file
    with open(instruction, "r") as f:
        instruction_text = f.read()

    with open(taxonomy, "r") as f:
        taxonomy_text = f.read()

    # 2. Combine the contents
    combined_text = instruction_text + "\n\n" + taxonomy_text
    
    return combined_text

def main():
    load_config()  # Load the configuration file
    config = get_config() 

    
    taxonomy = f'./main_input/iab_definitions.txt' 
    instruction = f'./main_input/Instruction.txt'    
    source_file = f'./main_input/data.csv' #input file
    
    output_folder = f'./outputs_{datetime.now().strftime("%Y%m%d_%H%M%S")}'    
          
    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist
    
    prompt = create_prompt(instruction,taxonomy)    
    
    data = pd.read_csv(source_file)
    n_rows = rows = data.shape[0]
          
    
    print('start classification....')
    result = cl.classification(config, prompt, data)    
    print('Classification finished!')
    print(f'analysis {data.shape[0]} videos and generated {result.shape[0]} classified vides')
    print('------------')
         
    
    result.to_csv(f'{output_folder}/result.csv')    

    

if __name__ == "__main__":   
    load_config()  # Load the configuration file
    config = get_config() 
    main()

    
