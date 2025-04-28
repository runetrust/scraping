import requests
import subprocess
import json
import re
import os
from bs4 import BeautifulSoup

'''
For this to work you need TruthBrush ("https://github.com/stanfordio/truthbrush") as this is what is run using SubProcess
For now, I am unsure how many posts are returned from the fetch, as this is not immediately clear from TruthBrush documentation.

You need to set up a .env file with login credentials to run this.

I have reduced the rate limit to 150 from 300 in the api.py file from Truthbrush, as I experienced
A temporary ban of my user with the default limit. If you are running this, this is a consideration
You should also make beforehand.
'''

all_posts = []

def fetch_posts():
    # This is syntax (program to run using subprocess, command to initiate, Truth Social user handle)
    result = subprocess.run(['truthbrush', 'statuses', 'realDonaldTrump'], capture_output=True, text=True)
    output = result.stdout
    # Creating separate json objects for each post for further analysis
    for line in output.splitlines():
        obj = json.loads(line)
        content = obj["content"]
        soup = BeautifulSoup(content, "html.parser")
        pure_post = soup.get_text()#separator="\n") 
        all_posts.append(pure_post)
    return(pure_post)

# Right now straight copy paste from other scrape script as this should work as a basis for saving to file
def save_scraped_text(raw_text, identifier, base_directory='scraped_truths', prefix='post'):
    """
    Save scraped text to file.
    
    Args:
        raw_text (str): The text content to be saved
        identifier (str): A unique identifer for filename.
        base_directory (str, optional): Directory to save text files. Defaults to 'scraped_truths'.
        prefix (str, optional): Prefix for the filename. Defaults to 'post'.
    
    Returns:
        str: Full path to the saved file
    """
    # Create the base directory if it doesn't exist
    os.makedirs(base_directory, exist_ok=True)
    
    # Generate a timestamped filename
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

fetch_posts()

for truth in all_posts:
    # The looping variable is terrible right now but it is late - This is the biggest fix needed right now
    looping_variable = truth[0]
    save_scraped_text(truth, identifier=looping_variable)