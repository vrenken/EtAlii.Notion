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
    print("Initialized Google library")


def get_new_patents():
    print("Fetching patents from Google")

    main_url = "https://patents.google.com/"

    res = requests.get(main_url + "xhr/query?url=q%3Dmetaverse%26num%3D100%26oq%3Dmetaverse%26sort%3Dnew&exp=&tags=")
    main_data = res.json()
    data = main_data['results']['cluster'][0]['result']

    items = list()

    for entry in data:
        item = entry['patent']
        item['Id'] = item['publication_number']
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

        items.append(item)

    return items


def remove_html_tags(text):
    import re
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)