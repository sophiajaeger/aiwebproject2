import os 
import requests
import re
import sys
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT
from whoosh import qparser, analysis, scoring

# Increase the recursion limit if necessary
sys.setrecursionlimit(10000)

ana = analysis.StandardAnalyzer(stoplist=None, minsize=1) # used to not exclude stopwords

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
        print("Get ",url)

        try:
            r = requests.get(url)
            if r.status_code != 200:
                print(f"Failed to fetch {url} (Status: {r.status_code})")
                continue

            soup = BeautifulSoup(r.content, 'html.parser') # parse the HTML content
            
            # Extract and count words from the page
            page_content = soup.get_text(separator='')
            page_title = soup.title.string if soup.title else "No title"
            
            """# Extract the first 50 words for the teaser
            words = page_content.split()
            teaser_words = words[:50]
            page_teaser = ' '.join(teaser_words)
            # Find the position of the 50th word in the original content
            teaser_end_pos = page_content.find(page_teaser) + len(page_teaser)
            # Extend the teaser to complete the sentence
            remaining_text = 'REMAINDER:'+ page_content[teaser_end_pos:]
            sentence_end = re.search(r'[.!?]', remaining_text)
            if sentence_end:
                page_teaser += remaining_text[:sentence_end.end()]"""
            
            # Extract the first three sentences for the teaser
            sentence_endings = re.finditer(r'[.!?]', page_content[:1000])
            end_positions = [match.end() for match in sentence_endings]
            if len(end_positions) >= 3:
                teaser_end_pos = end_positions[2]
            elif len(end_positions) > 0:
                teaser_end_pos = end_positions[-1]
            else:
                teaser_end_pos = len(page_content)
            page_teaser = page_content[:teaser_end_pos]

            writer.add_document(
                url=url,
                title=page_title,
                content=page_content.lower(),
                teaser=page_teaser
            )

            # Extract links from the page and add them to the agenda
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']  # get URL from the anchor tag
                found_url = normalize_url(href, prefix)
                """if href.startswith('http'):
                    found_url = href
                else:
                    found_url = prefix + href.lstrip('/')
                    """
                # add url to the agenda if it hasn't been processed yet
                if found_url.startswith(prefix) and found_url not in crawled_pages:
                    agenda.append(found_url)
        except Exception as e:
            print(f"Error while processing {url}: {e}")

    writer.commit()  # commit changes to the index
    print("Crawling completed!")

#to crawl seperated from the search (python crawler.py starts the crawler direct)
if __name__ == "__main__":
    prefix = 'https://vm009.rz.uos.de/crawl/' # 'https://interestingfacts.com/'
    start_url = prefix + 'index.html' #input("Enter the start URL (default: index.html): ") or prefix + 
    crawl(start_url, prefix)

"""
# Example search
print("\nSearch Results:")
print(search("las platipus"))
"""