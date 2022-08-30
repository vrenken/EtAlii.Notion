# EtAlii.Notion

Simple script to add patents from Google into a Notion database.

Required are two environment variables:

- NOTION_INTEGRATION_TOKEN
- NOTION_PATENT_DATABASE_ID

The target database should have the following columns:

- Id                  (Type = Title)
- Title               (type = Text)
- Url                 (type = Url)
- Publication date    (type = Date)
- Filing date         (type = Date)
- Assignee            (type = Text)
- Inventor            (type = Text)

