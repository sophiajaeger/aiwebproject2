import os
from whoosh.index import open_dir
from whoosh import qparser, scoring

#open or create the index directory
def get_or_create_index():
    if not os.path.exists("indexdir"):
        raise Exception("Index directory does not exist. Please run the crawler first.")
    return open_dir("indexdir")

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