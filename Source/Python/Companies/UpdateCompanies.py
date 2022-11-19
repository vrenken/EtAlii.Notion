import os
import asyncio
import Notion
from Notion2 import Notion2

import urllib.request
from urllib.parse import urlsplit, urlunsplit, quote

from pathlib import Path

async def main():

    global data_folder
    data_folder = f"Data/Images"
    Path(data_folder).mkdir(parents=True, exist_ok=True)

    Notion.init()

    notion2 = Notion2(Notion.notion_integration_token)

    print(f"Loading companies...")
    companies = Notion.get_all_companies()
    print(f"Found {len(companies)} companies")

    companies = sorted(companies, key=lambda c: Notion.get_string(c['properties']['Name']).strip())

    for company in companies:
        id = company['id']
        name = Notion.get_string(company['properties']['Name']).strip()
        image = Notion.get_string(company['properties']['Image']).strip()
        image = iri2uri(image)

        print(f"{id}: {name}")

        if image != '':
            fileName = f"{data_folder}/{id}.jpg"

            opener = urllib.request.URLopener()
            opener.addheader('User-Agent', 'Mozilla/5.0')
            filename, headers = opener.retrieve(image, filename=fileName)
            print(f"Stored: {filename}")

            children = Notion.get_page_children(id)
            if len(children) == 0:
            # if all(child['type'] != 'image' for child in children):
                print(f"Updating image on: {name}")
                notion2.image_add(id, image)

                if company['icon'] == None:
                    print(f"Updating icon on: {name}")
                    Notion.update_icon(id, image)

def iri2uri(iri):
    """
    Convert an IRI to a URI (Python 3).
    """
    uri = ''
    if isinstance(iri, str):
        (scheme, netloc, path, query, fragment) = urlsplit(iri)
        scheme = quote(scheme)
        netloc = netloc.encode('idna').decode('utf-8')
        path = quote(path)
        query = quote(query)
        fragment = quote(fragment)
        uri = urlunsplit((scheme, netloc, path, query, fragment))

    return uri

asyncio.get_event_loop().run_until_complete(main())