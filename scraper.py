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


def clean_dataframe(df):
  """
  Cleans the input DataFrame by renaming columns and dropping unnecessary ones.

  Args:
      df (pandas.DataFrame): The DataFrame to clean.

  Returns:
      pandas.DataFrame: The cleaned DataFrame.

  Example:
      df_cleaned = clean_dataframe(df)
      print(df_cleaned.head())
  """
  if df is None:
    return None


  # Define a list of columns to keep
  keep_columns = ["job_title",
      "job_employment_type",
      "job_description",
      "job_apply_link", 
      "job_publisher",
      "job_posted_at_datetime_utc",
      "employer_name",
      "employer_website",
      "job_country", 
      "job_city",
      "job_state",      
      "job_is_remote",
      "job_offer_expiration_datetime_utc",
      "job_required_skills",
      "job_min_salary",
      "job_max_salary",
      "job_required_experience.required_experience_in_months",
      "job_required_experience.experience_preferred",
      "job_highlights.Qualifications",
      "job_highlights.Responsibilities",
      "job_highlights.Benefits"]

  # Drop unnecessary columns
  columns_to_drop = [col for col in df.columns if col not in keep_columns]
  df = df.drop(columns=columns_to_drop,errors='ignore')

  # Rename columns list
  new_columns = {
      "job_title": "job_title",
      "job_employment_type": "employment_type",
      "job_description": "description",
      "job_required_skills": "required_skills",
      "job_required_experience.experience_preferred": "experience_preferred",
      "job_required_experience.required_experience_in_months": "required_experience_in_months",
      "job_highlights.Qualifications": "qualifications",
      "job_highlights.Responsibilities": "responsibilities",
      "job_highlights.Benefits": "benefits",
      "job_min_salary": "minimum_salary",
      "job_max_salary": "maximum_salary",   
      "job_country": "country", 
      "job_city": "city",
      "job_state": "state",   
      "job_is_remote": "is_remote",
      "job_apply_link": "apply_link", 
      "job_publisher": "job_publisher",
      "job_posted_at_datetime_utc": "date_posted",
      "job_offer_expiration_datetime_utc": "date_expires",
      "employer_name": "company_name",
      "employer_website": "company_website",
  }

  # Re-order columns
  df = df.reindex(columns=list(new_columns.keys()))

  # Rename columns
  df = df.rename(columns=new_columns)

  return df
