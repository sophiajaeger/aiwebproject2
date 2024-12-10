import requests
from bs4 import BeautifulSoup

prefix = 'https://vm009.rz.uos.de/crawl/'

start_url = prefix+'index.html'

agenda = [start_url]
crawled_pages = []
results = {}

while agenda:
    url = agenda.pop() # crawl the last page in the agenda
    crawled_pages.append(url) # add it to the list of crawled pages so that infinite loop is created when pages backlink
    print("Get ",url)
    r = requests.get(url)
    print(r, r.encoding)
    if r.status_code == 200:
        soup = BeautifulSoup(r.content, 'html.parser')
        for word in soup.get_text().split():
            if word.lower() in results.keys():
                results[word.lower()].append(url)
            else:
                results[word.lower()] = [url]
        for anchor in soup.find_all('a'):
            # to do: only use page links that are on the prefix server
            if ('www.' or 'http') not in str(anchor):
                found_url = prefix+anchor.get('href') 
                if found_url not in crawled_pages:
                    agenda.append(found_url) 


print(results['the'])
    




