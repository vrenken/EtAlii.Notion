import requests
import html
from bs4 import BeautifulSoup
from google_patent_scraper import scraper_class
import json
import logging
import os
import pprint
import time


def init():
    global patent_searches
    patent_searches = os.getenv('NOTION_PATENT_SEARCHES')
    if patent_searches is None:
        raise ValueError("Please assign semicolon-separated patent searches to the 'NOTION_PATENT_SEARCHES' environment variable.")
    patent_searches = patent_searches.split(';')
    print("Initialized Google library")


def get_new_patents():

    main_url = "https://patents.google.com/"

    items = list()

    for patent_search in patent_searches:

        print(f"Fetching newest patents from Google for search: {patent_search}")
        normal_query = f"xhr/query?url=q%3D%22{patent_search}%22%26oq%3D%22{patent_search}%22&exp=&tags="
        res = requests.get(main_url + normal_query)
        main_data = res.json()
        data = main_data['results']['cluster'][0]['result']
        for entry in data:
            item = build_result_patent(entry, patent_search, main_url)
            items.append(item)

        print(f"Fetching best patents from Google for search: {patent_search}")
        newest_query = f"xhr/query?url=q%3D%22{patent_search}%22%26num%3D100%26oq%3D%22{patent_search}%22%26sort%3Dnew&exp=&tags="
        res = requests.get(main_url + newest_query)
        main_data = res.json()
        data = main_data['results']['cluster'][0]['result']
        for entry in data:
            item = build_result_patent(entry, patent_search, main_url)
            items.append(item)

    return items


def build_result_patent(entry, patent_search, main_url):
    item = entry['patent']
    item['Id'] = item['publication_number']
    item['Type'] = patent_search
    item.pop('publication_number')
    item['Url'] = main_url + "patent/" + item['Id'] + "/en"

    print(f"Fetching patent from Google: {item['Id']}")

    details_page_request = requests.get(item['Url'])
    parsed_details_page = BeautifulSoup(details_page_request.text, 'html.parser')
    metas = parsed_details_page.find_all("meta")
    metas = list(filter(lambda m: "name" in m.attrs, metas))
    metas = list(filter(lambda m: m["name"] == "DC.title", metas))
    title = metas[0]["content"]
    item['Title'] = remove_html_tags(title)
    item['Title'] = html.unescape(item['Title']).strip()
    item.pop('title')

    item['Inventor'] = item['inventor']
    item.pop('inventor')
    item['Assignee'] = item['assignee']
    item.pop('assignee')

    item['Filing date'] = item['filing_date']
    item.pop('filing_date')
    item['Publication date'] = item['publication_date']
    item.pop('publication_date')
    return item


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)