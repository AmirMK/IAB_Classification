
# Ad Classification and Video Analysis

This repository contains scripts and resources for classifying video ads using Gemini and processing the results. The workflow involves reading inputs, sending video ads for classification, and generating structured output files.

---

## **Project Structure**

```plaintext
main_input/
    ├── Instruction.txt      # Instructions for Gemini
    ├── iab_definitions.txt  # Full list of IAB categories in Levels 1, 2, and 3
    ├── data.csv             # Input data containing video information

output_timestamped/
    └── [results].csv  # Output folder for results

classification.py  # Contains supporting methods for ad classification
video_analysis.py  # Main script for processing and analysis
```
## Input Files

### Instruction.txt
- **Purpose:**  
  Provides the classification instructions for Gemini to process video ads.

- **Details:**  
  This file contains detailed instructions on how Gemini should classify the videos.

---

### iab_definitions.txt
- **Purpose:**  
  Contains the full list of IAB categories across three hierarchical levels (Level 1, Level 2, and Level 3).

- **Details:**  
  Each line corresponds to a category definition, providing a structured hierarchy for classification.

---

### data.csv
- **Purpose:**  
  The primary input file for video classification.

- **Required Columns:**  
  - **Id:** A unique identifier for each video.  
  - **gcs_fn:** The Google Cloud Storage (GCS) URL for the video file.

---

## Code Files

### classification.py
This file contains all the supporting methods required for ad classification. Below are the key functions:

#### **call_gemini**
- **Purpose:**  
  Sends video ads to Gemini and retrieves the response in a predefined JSON schema.

- **Input:**  
  - Video file URL (from `data.csv`)  
  - Instructions (from `Instruction.txt`)

- **Output:**  
  - JSON response containing classification results for the video ad.

---

#### **run_multiple_times**
- **Purpose:**  
  Handles concurrent calls to Gemini, enabling efficient processing of multiple videos.

- **Details:**  
  Ensures that video ads are processed simultaneously, reducing latency and speeding up overall classification.

---

#### **candidate_count_handler**
- **Purpose:**  
  Processes multiple outputs from Gemini for the same video and determines the most frequent value for each key.

- **Details:**  
  - Retrieves multiple classification candidates.  
  - Selects the most frequent classification for each key in the output JSON.

---

### video_analysis.py
This is the main script that orchestrates the entire workflow, integrating input processing, classification, and output generation.

#### Workflow Overview
1. **Input Reading:**  
   - Reads input files from the `main_input` folder (`Instruction.txt`, `iab_definitions.txt`, and `data.csv`).

2. **Classification:**  
   - Utilizes functions in `classification.py` to process videos through Gemini.  
   - Handles concurrent calls and candidate resolution.

3. **Output Generation:**  
   - Results are stored in a Pandas DataFrame.  
   - The final output is saved as a timestamped CSV file in the `output` folder.

---

## Output

- **Format:**  
  A CSV file containing classification results for each video.

- **Location:**  
  Saved in the `[YYYY-MM-DD_HH-MM-SS]_output/` subfolder with a filename in the format:  
  `results.csv`
