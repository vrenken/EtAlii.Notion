import asyncio

import Keywords
import Google
import Notion


async def main():

    Keywords.Init()
    Notion.init()
    Google.init()

    patents_in_google = await Google.get_new_patents()

    for patent_in_google in patents_in_google:
        has_patent_in_notion = Notion.has_patent(patent_in_google)
        if has_patent_in_notion:
            print(f"Skipping: {patent_in_google['Id']} - {patent_in_google['Title']}")
        else:
            print(f"Adding:   {patent_in_google['Id']} - {patent_in_google['Title']}")
            Notion.add_patent(patent_in_google)

asyncio.get_event_loop().run_until_complete(main())