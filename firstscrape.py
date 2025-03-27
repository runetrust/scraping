import requests
import re
import concurrent.futures
from bs4 import BeautifulSoup

# Theoretically scales infinitely, current fetch takes about ~ 10 seconds
url_list = ["https://www.ft.dk/da/dokumenter/dokumentlister/referater?pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20231&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20221&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20222&pageSize=200",
            "https://www.ft.dk/da/dokumenter/dokumentlister/referater?session=20211&pageSize=200"
            ]

def fetch_url(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response
    except requests.exceptions.RequestException as e:
        print(f"Error fetching page: {e}")
        return none

def fetch_all_urls(urls, max_workers = 10):
        # This allows for parallel fetches, much faster than standard for loop
        with concurrent.futures.ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Map the fetch_url function to all URLs
            responses = list(executor.map(fetch_url, urls))
        # Only returning succesful fetches
        return [response for response in responses if response is not None]

responses = fetch_all_urls(url_list)

all_docs_list = []

# Iterating over all links in url_list and making the into a soup object for parsing
for response in responses:
    soup = BeautifulSoup(response.content, "html.parser")
    # Find all links with the document link class
    all_docs = soup.find_all("a", class_="column-documents__link")
    # List comprehension to account for the list object returned by find_all()
    partial_links = [doc.get("href") for doc in all_docs]
    # Filter out only "forhandlinger", as the others seem to be videos only
    docs = [link for link in partial_links if "forhandlinger" in link]
    # Adding the results to the empty list
    all_docs_list.extend(docs)

# Keeping only every other index by slicing, for some reason all objects were returned twice in OG call
all_docs_sliced = docs[::2]

# Iterate through the found links and print them (currently), in future this gets parsed through regex / NLP to only have raw text
for doc in all_docs_sliced:
    print(f"https://www.ft.dk{doc}")

print(f"Number of constructed links is {len(all_docs_list)}")


