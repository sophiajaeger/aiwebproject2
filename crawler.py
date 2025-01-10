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
            page_content = soup.get_text()
            page_title = soup.title.string if soup.title else "No title"
            
            # Extract the first 50 words for the teaser
            words = page_content.split()
            teaser_words = words[:50]
            page_teaser = ' '.join(teaser_words)
            # Find the position of the 50th word in the original content
            teaser_end_pos = page_content.find(page_teaser) + len(page_teaser)
            # Extend the teaser to complete the sentence
            remaining_text = page_content[teaser_end_pos:]
            sentence_end = re.search(r'[.!?]', remaining_text)
            if sentence_end:
                page_teaser += remaining_text[:sentence_end.end()]

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

def search(query_str):
    """
    Parameter: query_str (string)
    Return: list of results
    Takes a query and searches the results dictionary for the urls containing the words and 
    returns their URL, title, count
    """
    ix = get_or_create_index()
    search_results = []
    seen_urls = set()
    suggestions = []
    print("searching for", query_str)
    
    with ix.searcher(weighting=scoring.TF_IDF()) as searcher:
        or_group = qparser.OrGroup.factory(0.8) # make results score higher that include multiple words in the query, but also include those that dont include all words
        parser = qparser.MultifieldParser(["title", "content"], schema=ix.schema, group=or_group)
        query = parser.parse(query_str)
        results = searcher.search(query, scored=True, limit=10)
        
        # add search results to the list
        for result in results:  
            url = result["url"]
            if url not in seen_urls:
                seen_urls.add(result['url'])
                search_results.append({
                            "url": url,
                            "title": result["title"],
                            "teaser": result["teaser"],
                            "count": result.score
                    })
                
        
        # search for a better query string
        corrected = searcher.correct_query(query, query_str, prefix=1) # each word must have at least the first letter in common with the word in the original query to speed up search
        if corrected.query != query:
            corrected_results = searcher.search(corrected.query, scored=True)
            # decide whether to show the suggested corrected query
            if not search_results or (len(search_results) < 3 and len(corrected_results) >= 3) or corrected_results[0].score > search_results[0]['count']:
                suggestions = [corrected.string]
            
    return search_results, suggestions

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