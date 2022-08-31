import string
from glob import glob
import asyncio
from pathlib import Path
from os.path import exists
from pyppeteer import launch

def Init():
    global printable_characters
    printable_characters = set(string.printable)

async def retrieve_patent_keywords(patent_url, patent_id):

    folder = f"Downloads/{patent_id}"
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
# patent_url = "https://patents.google.com/patent/US20220242450A1/en"
# asyncio.get_event_loop().run_until_complete(retrieve_patent_keywords(patent_url, "CN114780868A"))

