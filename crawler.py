import requests

from bs4 import BeautifulSoup

from whoosh.index import create_in
from whoosh.fields import *
# import os

# Define the schema for the Whoosh index
schema = Schema(
    url=ID(stored=True, unique=True),  # Store URLs (unique identifier)
    title=TEXT(stored=True),  # Store and index titles
    content=TEXT,  # Index full text content (not stored to save space)
    teaser=TEXT(stored=True)  # Store the teaser for display
)

ix = create_in("indexdir", schema)
writer = ix.writer()

prefix = 'https://vm009.rz.uos.de/crawl/'

start_url = prefix +'index.html'

agenda = [start_url]
crawled_pages = []
global results 
results = defaultdict(lambda: defaultdict(int))  # a nested dictionary for words and their counts on urls

while agenda:
    url = agenda.pop() # crawl the last page in the agenda
    if url in crawled_pages:  # to make sure that there are no double 
        continue
    
    crawled_pages.append(url) # add it to the list of crawled pages so that infinite loop is created when pages backlink
    print("Get ",url)
    r = requests.get(url)
    print(r, r.encoding)

    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser') # parse the HTML content
        
        #extract and count words from the page
        """for word in soup.get_text().lower().split():
            if url not in results[word]:
                results[word][url] = {
                    "count": 0,
                    "title": soup.title.string if soup.title else "No Title", # page titel
                    "teaser": soup.get_text()[:200] #first 200 characters of the page text
                }
            results[word][url]["count"] += 1 #increment the word count"""

        # Add the document to the Whoosh index
    writer.add_document(
        url=url,
        title=page_title,
        content=page_content,
        teaser=page_teaser
    )

    # Commit the writer after processing
    writer.commit()

    for anchor in soup.find_all('a'):
            # to do: only use page links that are on the prefix server
            href = anchor.get('href') #get URL from the anchor tag
            print('href type', type(href), href)
            found_url = '' 
            if prefix in href:
                found_url = href
            elif 'www' not in href and 'http' not in href:
                found_url = prefix + href
            # add url to the agenda if it hasn't been processed yet
            if len(found_url)!=0 and found_url not in crawled_pages and found_url not in agenda:
                agenda.append(found_url)

            """
            found_link = anchor.get('href')
            if prefix in anchor:
                if found_link not in crawled_pages:
                    agenda.append(found_link) # test if there yet?
            elif ('www.' or 'http') not in str(anchor):
                found_url = prefix+anchor.get('href') 
                if found_url not in crawled_pages:
                    agenda.append(found_url) """

def search(word_list):
    """
    Parameter: list (of word, all in lowercase letters)
    Return: list of results
    Takes a list of words and searches the results dictionary for the urls containing the words and 
    returns their URL, title, count
    """
    search_results = []
    for word in word_list:
        if word in results:
            for url, data in results[word].items():
                search_results.append({
                    "url": url,
                    "title": data["title"],
                    "teaser": data["teaser"],
                    "count": data["count"]
                })
    return search_results


# Print results (all words, URLs and the metadate - URL, title, count)
for word, urls in results.items():
    for url, data in urls.items():
        print(f"'{word}' found {data['count']} times on {url}")