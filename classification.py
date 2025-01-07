import pandas as pd
import numpy as np
import time
import math
import pickle
import random
from collections import Counter

import json
import base64
import vertexai
from vertexai.generative_models import GenerativeModel, SafetySetting, Part,GenerationConfig
from concurrent.futures import ThreadPoolExecutor, as_completed

def candidate_count_handeler(responses):
    candidates = responses.candidates  # Replace with your actual data

    # Initialize a dictionary to count frequencies of values for each key
    key_value_counts = {}

    for candidate_ in candidates:
        candidate = json.loads(candidate_.text)
        for key, value in candidate.items():
            key_value_counts.setdefault(key, Counter())[value] += 1

    # Create the final dictionary with the most frequent value for each key
    final_dict = {
        key: random.choice([val for val, freq in counts.items() if freq == max(counts.values())])
        for key, counts in key_value_counts.items()
    }
    
    return final_dict

    
def call_gemini(index, text_prompt,video_url): 
    
    response_schema = {
          "type": "object", 
          "properties": {
            "IAB_Category": {
                "type": "STRING"
            },
            "Advertiser_Domain": {
                "type": "STRING"
            },
            "Ad_Sensitivity": {
                "type": "STRING",
                "enum": ['True', 'False']
            },
            "Ad_Severity": {
                "type": "STRING",
                "enum": ['High', 'Medium','None']
            },
            "Advertiser": {
                "type": "STRING"
            },
            "Ad_Language": {
                "type": "STRING"
            },
            "IAB_Category_Reasoning": {
                "type": "STRING"
            },
            
          },
          "required": ["IAB_Category","Advertiser_Domain","Ad_Sensitivity",
                       "Ad_Language","Advertiser","Ad_Severity","IAB_Category_Reasoning"]
        }
    
    vertexai.init(project="vertex-ai-search-v2", location="us-central1")
    
    generation_config = GenerationConfig(
    max_output_tokens= 8192,
    temperature= 0.0,
    candidate_count = 3,
    seed=0,
    response_mime_type = "application/json",
    response_schema=response_schema
)

    video = Part.from_uri(
    mime_type="video/mp4",
    uri=video_url,
    )

    
    model = GenerativeModel(
        "gemini-1.5-pro-002",
        system_instruction=text_prompt
    )
    responses = model.generate_content(
        [video, "Please classify"],
        generation_config=generation_config,                
    )
    
    responses = candidate_count_handeler(responses)
    return index, responses

def run_multiple_times(data_df,prompt, url_column, Id_column , batch_size=5):
    # Initialize llm_responses to store results
    llm_responses = []

    # Prepare tasks with Id as the index
    tasks = [(row[Id_column], prompt,row[url_column]) for _, row in data_df.iterrows()]

    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(tasks), batch_size):
            #time.sleep(20)
            batch = tasks[i:i + batch_size]
            
            # Submit tasks to the executor
            futures = [
                executor.submit(call_gemini, Id, text, url) for Id, text, url in batch
            ]
            
            # Collect the results as they complete
            for future in as_completed(futures):
                Id = None  # Initialize Id to handle errors gracefully
                try:
                    # Extract the Id and generated images from call_gemini
                    Id, responses = future.result()
                    
                    # Store only the Id and images in llm_responses
                    llm_responses.append({
                        Id_column: Id,
                        "response": responses
                    })
                    
                except Exception as e:
                    print(f"Error processing prompt with Id {Id}: {e}")

    return llm_responses  

def classification(prompt, url_column,Id_column, data):    
    result=[]
    
    rows_per_sample = 10
    
    rows = data.shape[0]
    n = math.ceil(rows / rows_per_sample)  # Calculate n by rounding up
    
    sample_data_full = pd.DataFrame() 
    
    for i in range (n):
        start_idx = i * rows_per_sample
        end_idx = start_idx + rows_per_sample
        sample_data = data.iloc[start_idx:end_idx]

        sample_data_full = pd.concat([sample_data_full, sample_data], ignore_index=True)

        a = run_multiple_times(sample_data,prompt, url_column, Id_column , batch_size=5)        

        for item in a:
            result.append([item[Id_column],item['response']['IAB_Category'],
                          item['response']['Advertiser_Domain'],
                          item['response']['Ad_Sensitivity'],
                          item['response']['Ad_Severity'],
                          item['response']['Advertiser'],                          
                          item['response']['Ad_Language'],
                           item['response']['IAB_Category_Reasoning'],
                          ])
        
        
        
        print(f"Iteration {i+1} done and results saved.")
        
    result = pd.DataFrame(result,columns=[Id_column,'Gemini_Prediction','Advertiser_Domain','Ad_Sensitivity','Ad_Severity','Advertiser','Ad_Language','IAB_Category_Reasoning'])
    return result 

