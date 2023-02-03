import argparse
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from datetime import datetime

def fetch_url_content(url):
    res = requests.get(url)
    return res.text

def save_url_content(url, content):
    url_comp = urlparse(url)
    filename = url_comp.hostname + '.html'

    with open(filename, 'w') as web_file:
        web_file.write(content)

def extract_meta(url, content):
    meta = {}
    url_comp = urlparse(url)
    meta['site'] = url_comp.hostname
    meta['last_fetch'] = datetime.utcnow().isoformat()

    soup = BeautifulSoup(content, 'html.parser')
    content_links = soup.find_all('a') # find all links
    content_img = soup.find_all('img')
    
    meta['num_links'] = len(content_links)
    meta['images'] = len(content_img)
    
    return meta
    
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
        meta = extract_meta(url, content)
        print(meta)


