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
      "x-rapidapi-key": "insert-api-key-here",
	    "x-rapidapi-host": "jsearch.p.rapidapi.com"
  }
  json_name = "job_listings.json"
  csv_name = "job_listings.csv"

  # Extract and Download the JSON file
  #file_path = extract_listings(url, query, headers, filename=json_name)

  # Load the JSON data into a DataFrame
  #df = json_to_dataframe(json_name)
help(extract_listings)
  # Save the DataFrame to a CSV file

