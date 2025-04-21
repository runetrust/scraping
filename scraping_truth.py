import requests
import subprocess
import json
import re
import os
from bs4 import BeautifulSoup

'''
For this to work you need TruthBrush ("https://github.com/stanfordio/truthbrush") as this is what is run using SubProcess
For now, I am unsure how many posts are returned from the fetch, as this is not immediately clear from TruthBrush documentation.
Right now all posts are returned with HTML tags, which I would like to avoid in the future.
'''

def fetch_posts:
    # This is syntax (program to run using subprocess, command to initiate, Truth Social user handle)
    result = subprocess.run(['truthbrush', 'statuses', 'realDonaldTrump'], capture_output=True, text=True)
    output = result.stdout
    # Creating separate json objects for each post for further analysis
    for line in output.splitlines():
        obj = json.loads(line)
        content = obj["content"]
        soup = BeautifulSoup(content, "html.parser")
        #pure_post = 

        print(content)


'''
content = output["content"]

print(content)
'''