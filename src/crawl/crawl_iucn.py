import os
from datetime import date
from pydoc import doc
import time
import requests

from bs4 import BeautifulSoup
import dateparser
from dotenv import load_dotenv

load_dotenv()

# Local application imports
from metadata.document_metadata import *
from config import config

CORPUS_ID = 'IUCN'
ORGANIZATION = 'iucn.org'

def main():

    user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.97 Safari/537.36'

    head = {
        'User-Agent': user_agent,
        'Accept': 'application/pdf,text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'
    }

    #
    # First - scrape and parse all the 'container' pages
    #
    documents = []
    for url in load_urls_to_scrape(CORPUS_ID):
        document_meta = scrape_url(url, head)
        if document_meta:
            print(document_meta.title)
            documents.append(document_meta)

    # Save to Disk
    filename = f'{config.CORPUS_DIR}/{CORPUS_ID}/{config.DOCUMENT_METADATA_FILENAME}'
    save_document_metadata(filename, documents)

    #
    # Load the file back and download all the pdfs
    #
    for document in load_document_metadata(filename):
        download_document(document, head)


def load_urls_to_scrape(document_collection_name):
    filename = f'{config.CORPUS_DIR}/{document_collection_name}/seed_urls.txt'
    with open(filename, 'r') as fin:
        return [url.strip() for url in fin.readlines()]


def scrape_url(url, head):
    
    print('\n--------------------------------------')
    print(url)

    response = requests.get(
        url,
        proxies={
            'http': f'http://{os.environ.get("crawlera_api_key")}:@proxy.crawlera.com:8011/',
            'https': f'http://{os.environ.get("crawlera_api_key")}:@proxy.crawlera.com:8011/',
        },
        verify='/usr/local/share/ca-certificates/zyte-smartproxy-ca.crt'
    )

    soup = BeautifulSoup(response.text, 'html.parser')

    headers = ' '.join([normalize_whitespace(h.get_text()) for h in soup.find_all('h1')])
    paragraphs = ' '.join([normalize_whitespace(p.get_text()) for p in soup.select('div.field-type-text-with-summary')])
    
    article_date = None
    times = soup.select('span.date-display-single')
    if times:
        article_date = dateparser.parse(times[0]['content'])

    links = soup.select('div.download-icon')
    if links:
        link = links[0].find('a')
        href = link['href'].lower()
        print(f'Found download URL: {href}')
    
        if href.endswith('.pdf'):

            return DocumentMetadata(
                    generate_document_id(href),
                    CORPUS_ID,
                    ORGANIZATION,
                    href.split('/')[-1],
                    url,
                    href,
                    headers,
                    normalize_whitespace(paragraphs)[:1000],
                    article_date
                )


def normalize_whitespace(s):
    # Normalize all whitespace and newlines to a single line
    return ' '.join(s.split())


def download_document(document_meta, head):
    
    url = document_meta.download_url
    filename = config.get_document_raw_filename(document_meta.corpus_id, document_meta.local_filename)

    print('\n--------------------------------------')
    print(f'Downloading {url} to {filename}')

    response = requests.get(
        url,
        proxies={
            'http': f'http://{os.environ.get("crawlera_api_key")}:@proxy.crawlera.com:8011/',
            'https': f'http://{os.environ.get("crawlera_api_key")}:@proxy.crawlera.com:8011/',
        },
        verify='/usr/local/share/ca-certificates/zyte-smartproxy-ca.crt',
        stream=True
    )

    with open(filename, 'wb') as f:
        f.write(response.content)
  

if __name__ == "__main__":
    main()