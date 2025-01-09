# print("Loading crawler.py")
import os 
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT
from whoosh import qparser, analysis, scoring

ana = analysis.StandardAnalyzer(stoplist=None, minsize=1) # used to not exclude stopwords

# Define the schema for the Whoosh index
schema = Schema(
    url=ID(stored=True, unique=True),  # Store URLs (unique identifier)
    title=TEXT(stored=True),  # Store and index titles
    content=TEXT,  # Index full text content (not stored to save space)
    teaser=TEXT(stored=True)  # Store the teaser for display
)

# Index directory setup (create or open it)
if not os.path.exists("indexdir"):
    os.mkdir("indexdir")
    ix = create_in("indexdir", schema)
else:
    ix = open_dir("indexdir")

prefix = 'https://vm009.rz.uos.de/crawl/'
start_url = prefix +'index.html'
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
print("Indexing completed!")

def search(query_str):
    """
    Parameter: query_str (string)
    Return: list of results
    Takes a query and searches the results dictionary for the urls containing the words and 
    returns their URL, title, count
    """
    search_results = []
    print("searching for", query_str)
    # ix.searcher(weighting=scoring.TF_IDF())
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        or_group = qparser.OrGroup.factory(0.8) # make results score higher that include multiple words in the query, but also include those that dont include all words
        parser = qparser.MultifieldParser(["title", "content"], schema=ix.schema, group=or_group)
        query = parser.parse(query_str)
        results = searcher.search(query, scored=True, limit=10)
        
        # Debug: Print the raw search results
        print(f"Raw search results for '{query_str}':")
        for result in results:
            print(f"URL: {result['url']}, Score: {result.score}")
        
        # add search results to the list
        seen_urls = set()
        for result in results:  
            if result['url'] not in seen_urls:
                seen_urls.add(result['url'])
                search_results.append({
                            "url": result['url'],
                            "title": result["title"],
                            "teaser": result["teaser"],
                            "count": result.score
                    })
    return search_results

# Example search
print("\nSearch Results:")
print(search("do platypus eat"))