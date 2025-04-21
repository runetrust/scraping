import requests
import subprocess
import json
import re
import os
from bs4 import BeautifulSoup

def fetch_posts:
    result = subprocess.run(['truthbrush', 'statuses', 'realDonaldTrump'], capture_output=True, text=True)
    output = result.stdout
    for line in output.splitlines():
        obj = json.loads(line)
        content = obj["content"]
        soup = BeautifulSoup(content, "html.parser")
        pure_post = 

        #print(obj["content"])



'''
content = output["content"]

print(content)
'''