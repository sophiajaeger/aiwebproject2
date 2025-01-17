import os 
import requests
import re
import sys
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urldefrag
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT

# Define the schema for the Whoosh index
schema = Schema(
    url=ID(stored=True, unique=True),  # Store URLs (unique identifier)
    title=TEXT(stored=True, spelling=True),  # Store and index titles
    content=TEXT(spelling=True),  # Index full text content (not stored to save space)
    teaser=TEXT(stored=True, spelling=True)  # Store the teaser for display
)
# Initialize or open the Whoosh index
def get_or_create_index():
    if not os.path.exists("indexdir"):
        os.mkdir("indexdir")
        return create_in("indexdir", schema)
    return open_dir("indexdir")

def normalize_url(url, prefix):
    """Normalize URLs by adding the prefix if they are relative"""
    if url.startswith('http'):
        return url
    else:
        return prefix + url.lstrip('/')
    full_url = urljoin(prefix, url)
    clean_url, _ = urldefrag(full_url)  # Remove fragment identifiers
    return clean_url

def crawl(start_url, prefix):
    ix = get_or_create_index()
    agenda = [start_url]
    crawled_pages = set()

    writer = ix.writer()
    while agenda:
        """Crawl the pages in the agenda and extract the words from the page content"""
        url = agenda.pop() # crawl the last page in the agenda
        if url in crawled_pages:  # to make sure that there are no pages doubled
            continue
        
        crawled_pages.add(url) # add it to the set of crawled pages so that no infinite loop is created when pages backlink
        print("Get ",url, "(", len(crawled_pages)-1, "pages crawled so far)")

        try:
            r = requests.get(url)
            if r.status_code != 200:
                print(f"Failed to fetch {url} (Status: {r.status_code})")
                continue

            soup = BeautifulSoup(r.content, 'html.parser') # parse the HTML content

            # extract links from the page and add them to the agenda
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']  # get URL from the anchor tag
                found_url = normalize_url(href, prefix)
                # exclude unwanted URLs
                if 'cdn-cgi/l/email-protection' in found_url:
                    continue
                # add url to the agenda if it hasn't been processed yet
                if found_url.startswith(prefix) and found_url not in crawled_pages:
                    agenda.append(found_url)

            article = soup.find('article')
            if article:
                # extract title and description
                page_title = article.find('h1').get_text(strip=True)
                description_div = article.find('div', class_='description')
                if description_div:
                    description_paragraphs = description_div.find_all('p')
                    description_text = ' '.join(p.get_text(separator=' ', strip=True) for p in description_paragraphs)
                else:
                    description_text = ""  # no description found
                
                # extract all the text for the content
                content_paragraphs = article.find_all('p')
                page_content = ' '.join(p.get_text(separator=' ', strip=True) for p in content_paragraphs)

                # Use the description as the teaser
                page_teaser = description_text

            else: # if no article, fall back to general content
                page_title = soup.title.string if soup.title else "No title"
                # extract content from the main area
                main_content = soup.find('main')  
                if not main_content:  # if there's no <main>, fall back to body
                    main_content = soup.body
                
                content_paragraphs = main_content.find_all('p')  
                page_content = ' '.join(p.get_text(separator=' ', strip=True) for p in content_paragraphs)
                page_teaser = page_content[:450]  # first 450 characters as an initial teaser

            # Extract the first three sentences from the teaser
            sentence_endings = re.finditer(r'[.!?]', page_teaser)
            end_positions = [ending.end() for ending in sentence_endings]
            if len(end_positions) >= 3:
                teaser_end_pos = end_positions[2]
            elif len(end_positions) > 0:
                teaser_end_pos = end_positions[-1]
            else:
                teaser_end_pos = len(page_teaser)
            page_teaser = page_teaser[:teaser_end_pos]

            writer.add_document(
                url=url,
                title=str(page_title),
                content=str(page_content.lower()),
                teaser=str(page_teaser)
            )
            
        except Exception as e:
            print(f"Error while processing {url}: {e}")
    writer.commit()  # commit changes to the index
    print(f"Crawling completed! {len(crawled_pages)} pages found.")

#to crawl seperated from the search (python crawler.py starts the crawler direct)
if __name__ == "__main__":
    prefix = 'https://interestingfacts.com/' # 'https://vm009.rz.uos.de/crawl/' # 
    start_url = prefix + '' #'index.html' #input("Enter the start URL (default: index.html): ") or prefix + 
    crawl(start_url, prefix)