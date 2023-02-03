import argparse
import requests
from urllib.parse import urlparse

def fetch_url_content(url):
    res = requests.get(url)
    return res.text

def save_url_content(url, content):
    url_comp = urlparse(url)
    filename = url_comp.hostname + '.html'

    with open(filename, 'w') as web_file:
        web_file.write(content)    

parser = argparse.ArgumentParser(
    prog="Fetch-python",
    description="Gets and saves websites locally"
)

parser.add_argument("URLS", metavar='URL', type=str, nargs='+', help="URL(s) to be loaded and saved")

if __name__ == "__main__":
    args = parser.parse_args()
    urls = args.URLS

    for url in urls:
        content = fetch_url_content(url)
        save_url_content(url, content)


