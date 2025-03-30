import requests
import re
import os
import concurrent.futures
from bs4 import BeautifulSoup

# Theoretically scales infinitely, current fetch takes about ~ 10 seconds
url_list = ["https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20231&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20221&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20222&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20211&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20201",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20191",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20182",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20181",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20171",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20161",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20151",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20142",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20141",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20131",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20121",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20111",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20102",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20101",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20091",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20081",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20072",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20071",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20061",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20051",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20042",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200&session=20041"
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

def extract_date(text):
    # Pattern matches yyyy-mm-dd_HHHH format
    pattern = r"\/forhandlinger\/\d+\/\d+M\d+_(\d{4}-\d{2}-\d{2}_\d{4})\.htm" #r'(\d{4}-\d{2}-\d{2}-\d{4})
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    else:
        return None

def save_scraped_text(raw_text, date, base_directory='scraped_texts', prefix='meeting'):
    """
    Save scraped text to a file with a timestamped filename.
    
    Args:
        raw_text (str): The text content to be saved
        date (str): The date to the meeting
        base_directory (str, optional): Directory to save text files. Defaults to 'scraped_texts'.
        prefix (str, optional): Prefix for the filename. Defaults to 'meeting'.
    
    Returns:
        str: Full path to the saved file
    """
    # Create the base directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)
    
    # Generate a timestamped filename
    filename = f"{prefix}_{date}.txt"
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

all_docs_list = []

# Iterating over all links in url_list and making the into a soup object for parsing
for response in responses:
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all links with the document link class
    all_docs = soup.find_all("a", class_="column-documents__link")
    # List comprehension to account for the list object returned by find_all(), this returns all hyperlinks
    partial_links = [doc.get("href") for doc in all_docs]
    # Filter out only "forhandlinger", as the others seem to be videos only
    docs = [link for link in partial_links if "forhandlinger" in link]
    # Adding the results to the empty list
    all_docs_list.extend(docs)

# Keeping only every other index by slicing, for some reason all objects were returned twice in OG call
all_docs_sliced = all_docs_list[::2]

# Empty list for date extracted from the link of the document
document_date = []
# Empty variable for constructed links
constructed_links = []

# Iterate through the found links and construct a full link for further fetch and extract date from the link
for doc in all_docs_sliced:
    date = extract_date(doc)
    document_date.append(date)
    link = f"https://www.ft.dk{doc}"
    constructed_links.append(link)
print("Links constructed")

# Passing the constructed links to the fetch function again
print("Fetching all docs")
fetched_documents = fetch_all_urls(constructed_links)

# This now extracts all clean text and saves with a unique timestamp to prevent overwriting
print("Souping all docs and saving to file")
for document in fetched_documents:
     # Parsing
     soup = BeautifulSoup(document.content, "html.parser")
     # Extracting clean text and saving to file
     clean_text = soup.get_text()
     # Creating indexing variable as the data type was "response" from the requests package, this does not work as an iterable variable
     index = fetched_documents.index(document)
     save_scraped_text(raw_text=clean_text, date = document_date[index])

print("Finished scrape")