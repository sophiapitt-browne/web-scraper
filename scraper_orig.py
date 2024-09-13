import requests
import os
import pandas as pd
import json

# Extract and Download Job Listings
def extract_listings(url, query, headers, filename="job_listings.json"):
  """
  Fetches job listings from the RapidAPI APIs and downloads them as a JSON file.

  Args:
      url (str): The API endpoint URL.
      query (dict): The search query for jobs.
      headers (dict): The API headers.
      filename (str, optional): The name of the file to save the JSON data to. Defaults to "job_listings.json".

  Returns:
      str: The path to the downloaded JSON file, or None if an error occurred.

  Raises:
      requests.exceptions.RequestException: If an error occurs during the API request.

  Example:
      extract_listings(url, query, headers, filename="jobs.json")

  """

  try:
      response = requests.get(url, headers=headers, params=query)
      response.raise_for_status()  # Raise an exception for non-2xx status codes

      data = response.json()

      with open(filename, 'w') as json_file:
        json.dump(data, json_file, indent=4)

      print(f"Job listings downloaded successfully to {filename}")
      return filename

  except requests.exceptions.RequestException as e:
      print(f"Error downloading job listings: {e}")
      return None


# Convert Downloaded JSON File to a Pandas DataFrame
def json_to_dataframe(filename="jobs.json"):
  """Converts a JSON file containing job listings into a Pandas DataFrame.

  Args:
      filename (str, optional): The path to the JSON file. Defaults to "jobs.json".

  Returns:
      pandas.DataFrame: A DataFrame containing the job listing data.
      None: If an error occurs during file reading or DataFrame creation.

  Raises:
      FileNotFoundError: If the specified file is not found.
      json.JSONDecodeError: If there is an error decoding the JSON file.
  
  Example:
      df = json_to_dataframe('jobs.json')
      if df is not None:
          print(df.head())
  """

  try:
      with open(filename, 'r', encoding='utf-8') as f:
          data = json.load(f)

      # Check if the 'data' key exists and flatten nested dictionaries
      if 'data' in data:
          df = pd.json_normalize(data['data'])
      else:
          df = pd.json_normalize(data)
          #print("Error: 'data' key not found in JSON.")
          #return None
      return df
  except (FileNotFoundError, json.JSONDecodeError) as e:
      print(f"Error: {e}")
      return None

# Convert Dataframe to CSV file
def dataframe_to_csv(df, filename="jobs.csv"):
  """Converts a Pandas DataFrame to a CSV file.

  Args:
      df (pandas.DataFrame): The DataFrame to convert.
      filename (str, optional): The name of the CSV file to save. Defaults to "jobs.csv".

  Raises:
      Exception: If an error occurs during the saving process.

  Returns:
      str: The path to the saved CSV file.
      None: If an error occurs during the saving process.

  Example:
      df = pd.DataFrame('job_listings.json')
      dataframe_to_csv(df, 'output.csv')
  
  """
  try:
    # Check if the input is a DataFrame
    if not isinstance(df, pd.DataFrame):
      raise TypeError("Input must be a Pandas DataFrame.")

    # Save the DataFrame to a CSV file
    df.to_csv(filename, index=False)  # Set index=False to avoid saving the row index

    print(f"DataFrame saved to {filename}.")
    return filename

  except Exception as e:
    print(f"Error saving DataFrame to CSV: {e}")
    return None


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
