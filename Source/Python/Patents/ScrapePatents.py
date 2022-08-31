import Google
import Notion

Notion.init()
Google.init()

patent_searches = {
    "Metaverse",
    "Virtual Reality",
    "Mixed Reality",
    "Head Mounted Display"
}

patents_in_google = Google.get_new_patents(patent_searches)

for patent_in_google in patents_in_google:
    has_patent_in_notion = Notion.has_patent(patent_in_google)
    if has_patent_in_notion:
        print(f"Skipping: {patent_in_google['Id']} - {patent_in_google['Title']}")
    else:
        print(f"Adding:   {patent_in_google['Id']} - {patent_in_google['Title']}")
        Notion.add_patent(patent_in_google)
