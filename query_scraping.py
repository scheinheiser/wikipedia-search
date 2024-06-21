import requests
from bs4 import BeautifulSoup
# Necessary imports

BASE_LINK = 'https://en.wikipedia.org'
# The base link, onto which the extension will be added.

class ScrapingWebsite:
    def __init__(self, query, limit):
        # Sets the string to be searched and the amount of results to be displayed. It defaults to 20 if too low/high.
        self.query = query
        self.limit = limit if 5 <= limit <= 100 else 20

    def getting_results(self) -> list:
        wiki_page = requests.get(f'https://en.wikipedia.org/w/index.php?search={self.query}&title=Special:Search&limit={self.limit}&profile=advanced&fulltext=1&ns0=1')
        read_wiki = BeautifulSoup(wiki_page.content, features='html.parser')
        # Grabs the search page with the specific query and limit of results to be displayed.

        title_results = read_wiki.find_all(class_='searchResultImage-text')
        data_results = read_wiki.find_all(class_='mw-search-result mw-search-result-ns-0')
        description_results = read_wiki.find_all(class_='searchresult')
        returned_results = []
        # Establishes multiple variables that contain the specific html content for each part of the searched page.

        for results in range(len(title_results)):
            result_title = title_results[results].find('a').text
            for link in title_results[results].find_all('a'):
                result_link = f'{BASE_LINK}{link.get("href")}'

            result_desc = description_results[results].text
            result_data = data_results[results].find_all(class_='mw-search-result-data')[0].text

            returned_results.append((result_title, result_link, result_desc, result_data))
        # Finds the title, data, link and description and appends it to the results list.

        return returned_results # Returns the list for further use.