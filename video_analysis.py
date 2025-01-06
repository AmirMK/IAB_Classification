import pandas as pd
import numpy as np
import time
from datetime import datetime
import os

import json
import classification as cl

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
    taxonomy = f'./main_input/iab_definitions.txt' 
    instruction = f'./main_input/Instruction.txt'    
    source_file = f'./main_input/data_test.csv'
    
    
    output_folder = f'./outputs_{datetime.now().strftime("%Y%m%d_%H%M%S")}'    
       
    url_column = 'gcs_fn'
    Id_column = 'Id'   

    os.makedirs(output_folder, exist_ok=True)  # Create the directory if it doesn't exist
    
    prompt = create_prompt(instruction,taxonomy)    
    
    
    data = pd.read_csv(source_file)
    n_rows = rows = data.shape[0]
          
    
    print('start classification....')
    result = cl.classification(prompt, url_column,Id_column, data)    
    print('Classification finished!')
    print(f'analysis {data.shape[0]} videos and generated {result.shape[0]} classified vides')
    print('------------')
         
    
    result.to_csv(f'{output_folder}/result.csv')    

    

if __name__ == "__main__":    
    main()

    
