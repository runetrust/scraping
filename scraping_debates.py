import requests
import re
import os
import concurrent.futures
from bs4 import BeautifulSoup

url_list = [
    "https://www.debates.org/voter-education/debate-transcripts/september-29-2020-debate-transcript/",
    "http://debates.org/voter-education/debate-transcripts/vice-presidential-debate-at-the-university-of-utah-in-salt-lake-city-utah/",
    "https://www.debates.org/voter-education/debate-transcripts/october-22-2020-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-26-2016-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-4-2016-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-9-2016-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-19-2016-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-3-2012-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-11-2012-the-biden-romney-vice-presidential-debate/",
    "https://www.debates.org/voter-education/debate-transcripts/october-16-2012-the-second-obama-romney-presidential-debate/",
    "https://www.debates.org/voter-education/debate-transcripts/october-22-2012-the-third-obama-romney-presidential-debate/",
    "https://www.debates.org/voter-education/debate-transcripts/2008-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/2008-debate-transcript-2/",
    "https://www.debates.org/voter-education/debate-transcripts/october-7-2008-debate-transcrip/",
    "https://www.debates.org/voter-education/debate-transcripts/october-15-2008-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-13-2004-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-8-2004-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-5-2004-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-30-2004-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-3-2000-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-5-2000-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-11-2000-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-17-2000-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-17-2000-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-6-1996-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-9-1996-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-16-1996-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-11-1992-first-half-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-11-1992-second-half-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-13-1992-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-15-1992-first-half-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-15-1992-second-half-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-19-1992-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-25-1988-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-5-1988-debate-transcripts/",
    "https://www.debates.org/voter-education/debate-transcripts/october-13-1988-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-7-1984-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-11-1984-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-21-1984-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-21-1980-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-28-1980-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-23-1976-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-6-1976-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-22-1976-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/september-26-1960-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-7-1960-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-13-1960-debate-transcript/",
    "https://www.debates.org/voter-education/debate-transcripts/october-13-1960-debate-transcript/",
    "https://edition.cnn.com/2024/06/27/politics/read-biden-trump-debate-rush-transcript/index.html"
]

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return None
    
def fetch_all_urls(urls, max_workers = 10):
        # This allows for parallel fetches, much faster than standard for loop
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map the fetch_url function to all URLs
            responses = list(executor.map(fetch_url, urls))
        # Only returning succesful fetches
        return [response for response in responses if response is not None]

def save_scraped_text(raw_text, identifier, base_directory='scraped_debates', prefix='debate'):
    """
    Save scraped text to a file with a timestamped filename.
    
    Args:
        raw_text (str): The text content to be saved
        identifier (str): Unique identifier
        base_directory (str, optional): Directory to save text files. Defaults to 'scraped_debates'.
        prefix (str, optional): Prefix for the filename. Defaults to 'debate'.
    
    Returns:
        str: Full path to the saved file
    """
    # Create the base directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)
    
    # Generate a unique filename
    filename = f"{prefix}_{identifier}.txt"
    full_path = os.path.join(base_directory, filename)
    
    # Save the text with UTF-8 encoding to support various characters
    try:
        with open(full_path, 'w', encoding='utf-8') as file:
            file.write(raw_text)
        print(f"Text successfully saved to {full_path}")
        # Returning file path is useful for loading in data later
        return full_path
    except IOError as e:
        print(f"Error saving file: {e}")
        return None
    
responses = fetch_all_urls(url_list)

for document in responses:
     # Parsing
     soup = BeautifulSoup(document.content, "html.parser")
     # Extracting clean text and saving to file
     clean_text = soup.get_text()
     # Creating indexing variable as the data type was "response" from the requests package, this does not work as an iterable variable
     index = responses.index(document)
     save_scraped_text(raw_text=clean_text, identifier = index)