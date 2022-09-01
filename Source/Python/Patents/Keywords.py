import os
import string
from glob import glob
import asyncio
from pathlib import Path
from os.path import exists
from pyppeteer import launch
from keybert import KeyBERT

def init():
    global printable_characters
    printable_characters = set(string.printable)

    global data_folder
    data_folder = f"Data/"

    global text_folder
    text_folder = f"{data_folder}/Text"

    global keywords_folder
    keywords_folder = f"{data_folder}/Keywords"


def create_keywords():

    print("Extracting keywords")
    Path(keywords_folder).mkdir(parents=True, exist_ok=True)

    patent_folders = []

    for folder in Path(text_folder).glob("*"):
        patent_folders.append(folder)

    for patent_folder in patent_folders:

        patent_id = os.path.split(patent_folder)[-1]
        patent_file = f"{keywords_folder}/{patent_id}.txt"
        if not exists(patent_file):

            print(f"Extracting keywords for: {patent_id}")
            file_names = []
            for file_name in Path(patent_folder).glob("*"):
                file_names.append(file_name)

            content = ""
            for file_name in file_names:
                with open(file_name, 'r') as file:
                    data = file.read()
                    content += " " + data

            kw_model = KeyBERT()
            keywords = kw_model.extract_keywords(content)

            with open(patent_file, 'w') as f:
                for keyword, weight in keywords:
                    f.write(f"{keyword}\n")


async def retrieve_patent_keywords(patent_url, patent_id):

    folder = f"{text_folder}/{patent_id}"
    Path(folder).mkdir(parents=True, exist_ok=True)

    files = []

    for file in Path(folder).glob("*"):
        files.append(file)

    if len(files) == 0:
        print(f"Fetching patent text from Google: {patent_url}")

        browser = await launch()
        page = await browser.newPage()
        await page.goto(patent_url)

        parts_xpath = '//patent-text'
        texts_xpath = '//patent-text//section'

        parts = await page.xpath(parts_xpath)
        texts = await page.xpath(texts_xpath)
        
        i = 0
        while i < len(parts):
            part = await page.evaluate('(element) => element.getAttribute("name")', parts[i])
            text = await page.evaluate('(element) => element.textContent', texts[i])

            text = ''.join(filter(lambda x: x in printable_characters, text))

            file = f"{folder}/{part}.txt"
            with open(file, 'w') as f:
                f.write(text)

            i += 1

        await browser.close()

# local test
# patent_url = "https://patents.google.com/patent/CN114780868A/en?q=metaverse&oq=metaverse&sort=new"
# # patent_url = "https://patents.google.com/patent/US20220242450A1/en"

# init()
# asyncio.get_event_loop().run_until_complete(retrieve_patent_keywords(patent_url, "CN114780868A"))
# create_keywords()

