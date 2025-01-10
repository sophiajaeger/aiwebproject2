import os 
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT
from whoosh import qparser, analysis, scoring
from search import search #importsearch function

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
            page_content = soup.get_text().lower()
            page_title = soup.title.string if soup.title else "No title"
            page_teaser = page_content[:200]

            writer.add_document(
                url=url,
                title=page_title,
                content=page_content,
                teaser=page_teaser
            )

            # Extract links from the page and add them to the agenda
            for anchor in soup.find_all('a', href=True):
                href = anchor['href']  # get URL from the anchor tag
                if href.startswith('http'):
                    found_url = href
                else:
                    found_url = prefix + href.lstrip('/')
                # add url to the agenda if it hasn't been processed yet
                if found_url.startswith(prefix) and found_url not in crawled_pages:
                    agenda.append(found_url)
        except Exception as e:
            print(f"Error while processing {url}: {e}")

    writer.commit()  # commit changes to the index
    print("Crawling completed!")



#to crawl seperated from the search (python crawler.py starts the crawler direct)
if __name__ == "__main__":
    prefix = 'https://vm009.rz.uos.de/crawl/'
    start_url = prefix + 'index.html' #input("Enter the start URL (default: index.html): ") or prefix + 
    crawl(start_url, prefix)

"""
# Example search
print("\nSearch Results:")
print(search("las platipus"))
"""