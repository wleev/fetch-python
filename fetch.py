import argparse
import requests
from urllib.parse import urlparse, urljoin
from bs4 import BeautifulSoup
from datetime import datetime
from os import path
import os

def get_fetch_folder(url):
    url_comp = urlparse(url)
    return url_comp.hostname

def fetch_url_content(url):
    res = requests.get(url)
    return res.text

def save_url_content(url, content):
    folder = get_fetch_folder(url)
    if not path.exists(folder):
        os.mkdir(folder)

    filename = path.join(folder, 'index.html')
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


# extract link, img and script elements and change to local path
def parse_external_resources(content):
    soup = BeautifulSoup(content, 'html.parser')
    content_links = soup.find_all('link', href=True)
    content_img = soup.find_all('img', src=True)
    content_scripts = soup.find_all('script', src=True)

    resources = []
    for link in content_links:
        resources.append(link['href'])
        link['href'] = path.join('/resources', path.basename(link['href']))
    
    for img in content_img:
        resources.append(img['src'])
        img['src'] = path.join('/resources', path.basename(img['src']))

    for script in content_scripts:
        resources.append(script['src'])
        script['src'] = path.join('/resources', path.basename(script['src']))
    
    return soup.prettify(), resources

def download_external_resources(url, links):
    root_folder = get_fetch_folder(url)
    resource_folder = os.path.join(root_folder, 'resources')

    if not path.exists(resource_folder):
        os.mkdir(resource_folder)

    urlcomp = urlparse(url)
    root_url = ''
    root_url += urlcomp.scheme + '://' if urlcomp.scheme else ''
    root_url += urlcomp.netloc

    for link in links:
        try:
            # relative links needs hostname appended
            res_url = ''
            if urlparse(link).netloc == '':
                res_url = urljoin(root_url, link)
            else:
                res_url = link
            r = requests.get(res_url)
            res_filename = path.join(resource_folder, path.basename(link))
            print("downloading file: ", res_filename)
            open(res_filename, 'wb').write(r.content)
        except:
            print('Error downloading link: ', link)
    
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
        meta = extract_meta(url, content)
        print(meta)
        new_content, links = parse_external_resources(content)
        save_url_content(url, new_content)
        download_external_resources(url, links)



