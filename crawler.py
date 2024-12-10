import requests
from bs4 import BeautifulSoup

prefix = 'https://vm009.rz.uos.de/crawl/'

start_url = prefix+'index.html'

agenda = [start_url]
crawled_pages = []
global results 
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
            href = anchor.get('href')
            print('href type', type(href), href)
            found_url = '' 
            if prefix in href:
                found_url = href
            elif 'www' not in href and 'http' not in href:
                found_url = prefix + href
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
    Return: list
    Takes a list of words and searches the results dictionary for the urls containing the words
    """
    urls = []
    for word in word_list:
        if word in results.keys():
            urls

print(results['the'])
    




