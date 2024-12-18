import os
import requests
from bs4 import BeautifulSoup
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, ID, TEXT
from whoosh import qparser, analysis


ana = analysis.StandardAnalyzer(stoplist=None, minsize=1)
# Define Whoosh schema
schema = Schema(
    url=ID(stored=True, unique=True),
    title=TEXT(stored=True, analyzer=ana),
    content=TEXT(stored=True, analyzer=ana),
    teaser=TEXT(stored=True, analyzer=ana)
)

# Index directory setup
#if not os.path.exists("indexdir"):
os.mkdir("indexdir")
ix = create_in("indexdir", schema)  # Create index if it doesn't exist
#:
ix = open_dir("indexdir")  # Open existing index

# Crawler settings
prefix = 'https://vm009.rz.uos.de/crawl/'
start_url = prefix + 'index.html'

agenda = [start_url]
crawled_pages = set() 

writer = ix.writer()

print("Starting crawler...")

while agenda:
    url = agenda.pop()
    if url in crawled_pages:
        continue

    crawled_pages.add(url)
    print("Crawling:", url)

    try:
        response = requests.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch {url} (Status: {response.status_code})")
            continue

        soup = BeautifulSoup(response.content, 'html.parser')
        page_content = soup.get_text().lower()
        page_title = soup.title.string if soup.title else "No title"
        page_teaser = page_content[:200]

    
        # Extract and normalize links
        for anchor in soup.find_all('a', href=True):
            href = anchor['href']
            if href.startswith('http'):
                found_url = href
            else:
                found_url = prefix + href.lstrip('/')
            
            if found_url.startswith(prefix) and found_url not in crawled_pages:
                agenda.append(found_url)

        # Add the page to the Whoosh index
        writer.add_document(
            url=url,
            title=page_title,
            content=page_content,
            teaser=page_teaser
        )

    except Exception as e:
        print(f"Error while processing {url}: {e}")

# Commit changes to the index
writer.commit()
print("Indexing completed!")

# Search function with Whoosh
def search(query_str):
    search_results = []
    """
    Search for a query string in the Whoosh index.
    """
    print("searching for", query_str)
    with ix.searcher() as searcher:
        '''
        print("Indexed Documents:")
        for docnum in range(searcher.doc_count()):
            stored_fields = searcher.stored_fields(docnum)
            print(f"Document {docnum}: {stored_fields}")
        '''
        parser = qparser.QueryParser("content", ix.schema)
        query = parser.parse(query_str)
        #nächste zeile nur zum testen 
        print(f"Parsed Query: {query}")
        results = searcher.search(query)
        for result in results:
            #print("bin da")
            #print(url)
            '''if url not in search_results:
                print("bin hier")
                search_results.append({
                            "url":url,
                            "title":page_title,
                            "teaser":page_teaser
                            #count
                        })
            print("still searching")
            print(f"Title: {r['title']}")
            print(f"URL: {r['url']}")
            print(f"Teaser: {r['teaser']}")
            print("----------")'''
            search_results.append({
                            "url": result["url"],
                            "title": result["title"],
                            "teaser": result["teaser"],
                            "count": result.highlights("content").count(query_str)
            })
                
    return search_results
        

#return render_template("results.html", results=results, query=query)

#Example search
print("\nSearch Results:")
print(search("Platypus"))


