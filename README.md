# Entry Level Cybersecurity Jobs Web Scraper

This project contains Python code for extracting job listings from a RapidAPI API and converting the data into a Pandas DataFrame and CSV file.


## Installation

* Set up and activate a Python environment, for example:
```bash
python install -m venv scraper
```
```bash
.\scraper\scripts\activate
```    
* Extract files from the zip file or folder provided.

* Copy the extracted files to the new environment.

* Install the following libraries: `requests` and `pandas` via the provided requirements.txt file.
```bash
pip install -r requirements.txt
``` 


## Features and Functionality

The code defines three main functions stored in the scraper.py file:

* `extract_listings()`: Fetches job listings from the specified API endpoint using provided query parameters and headers, and saves the data to a JSON file.

* `json_to_dataframe()`: Converts a JSON file containing job listings into a Pandas DataFrame.

* `dataframe_to_csv()`: Converts a Pandas DataFrame to a CSV file.

* `clean_dataframe`: Cleans a DataFrame by renaming columns and dropping unnecessary ones (based on data from the Jsearch API).

These functions can be used together for the complete process of extracting the json data and converting to a CSV file or used separately to reduce the number of API requests or for further data analysis and cleaning purposes.

## Usage

A `main.py` file is also included which imports the `scraper.py` functions. You can edit this file or create other files to use the `scraper.py` functions by including:

```python
from scraper import *
```

1. **Set API parameters:**
   * Replace placeholders for `url`, `query`, and `headers` with your actual API endpoint, query, and headers.

2. **Customize file names:**
   * Modify `json_name` and `csv_name` variables to change the file names as needed.

3. **Calling the Functions:** 
   * Call the scraper functions with the necessary parameters, storing the results into variables.
   * Use help() to get more information about the scraper functions. e.g. `help(extract_listings)`

There is an optional `clean.py` file which can be used to remove unnecessary columns from the raw JSON file (works for the JSearch API only).

## Examples

Feel free to modify the query parameters and API details to extract listings from different APIs or to adjust the job search.

> **NOTE**  
> The scraper was tested on the [JSearch](https://rapidapi.com/letscrape-6bRBa3QguO5/api/jsearch) and [ActiveJobs](https://rapidapi.com/fantastic-jobs-fantastic-jobs-default/api/active-jobs-db) APIs but some APIs may require changes to the `extract_listings` or `json_to_dataframe` functions.


### Example 1. Complete Extraction Process (main.py)

This example demonstrates extracting job listings from the JSearch API and saving the results as "job_listings.json" and "job_listings.csv". Run the code in `main.py` to extract job listings, convert to DataFrame, and save as a CSV file.

```python
from scraper import *

# Run Function
if __name__ == "__main__":
  # Set Variables - JSearch
  url = "https://jsearch.p.rapidapi.com/search"

  query = {
      "query": "cybersecurity",
      "page": "1",
      "num_pages": "8",
      "date_posted": "all",
      "remote_jobs_only": "true",
  }

  headers = {
      "x-rapidapi-key": "803f7f4fd3msh5463766addfc2cbp13616ejsn2c2c3b21871b",
	    "x-rapidapi-host": "jsearch.p.rapidapi.com"
  }
  json_name = "job_listings.json"
  csv_name = "job_listings.csv"

  # Extract and Download the JSON file
  file_path = extract_listings(url, query, headers, filename=json_name)

  # Load the JSON data into a DataFrame
  df = json_to_dataframe(file_path)

  # Save the DataFrame to a CSV file
  if df is not None:
    dataframe_to_csv(df, csv_name)
  else:
    print("DataFrame conversion to CSV failed.")
```

### Example 2. Using an additional function to clean listings from the JSearch API (clean.py)

This example demonstrates extracting job listings from the downloaded JSON file "job_listings.json", dropping unnecessary columns and renaming columns before converting to a CSV. 
> **NOTE**  
> Note that the `clean.py` script assumes that there is an existing JSON file (to reduce the number of API requests). 

```python
from scraper import *

# Run Function
if __name__ == "__main__":
  # Set Variables - JSearch
  url = "https://jsearch.p.rapidapi.com/search"

  query = {
      "query": "cybersecurity",
      "page": "1",
      "num_pages": "8",
      "date_posted": "all",
      "remote_jobs_only": "true",
  }

  headers = {
      "x-rapidapi-key": "803f7f4fd3msh5463766addfc2cbp13616ejsn2c2c3b21871b",
	    "x-rapidapi-host": "jsearch.p.rapidapi.com"
  }
  json_name = "job_listings.json"
  csv_name = "cleaned_job_listings.csv"

  # Load the JSON data into a DataFrame
  df = json_to_dataframe(json_name)
  
  if df is not None:
  # Clean the DataFrame
    df_cleaned = clean_dataframe(df)
  # Save the DataFrame to a CSV file
    dataframe_to_csv(df_cleaned, csv_name)
  else:
    print("DataFrame conversion to CSV failed.")
```

