# EtAlii.Notion

Simple script to add patents from Google into a Notion database.

Before starting, make sure all required libraries are installed using pip.

for example:

```python
pip install bs4
pip install requests
pip install pyppeteer
pip install notion_database
pip install keybert
```

Also required are the following environment variables:

- NOTION_INTEGRATION_TOKEN
- NOTION_PATENT_DATABASE_ID
- NOTION_PATENT_SEARCHES

With Powershell these can be set using:

```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_INTEGRATION_TOKEN", "YOUR_NOTION_INTEGRATION_TOKEN")
[System.Environment]::SetEnvironmentVariable("NOTION_PATENT_DATABASE_ID", "YOUR_NOTION_PATENT_DATABASE_ID")
[System.Environment]::SetEnvironmentVariable("NOTION_PATENT_SEARCHES", "YOUR_NOTION_SEARCH_QUERIES")
```

The patent searches need to be semicolon separated, e.g.:

```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_PATENT_SEARCHES", "Healthcare;Medicine;Nanotechnology")
```

If you want to make a persist an environment variable for the current user profile:

```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_PATENT_DATABASE_ID", "YOUR_NOTION_PATENT_DATABASE_ID", [System.EnvironmentVariableTarget]::User)
```

The target database should have the following columns:

- Id                  (Type = Title)
- Title               (type = Text)
- Url                 (type = Url)
- Publication date    (type = Date)
- Filing date         (type = Date)
- Assignee            (type = Text)
- Inventor            (type = Text)
- Type                (type = Select)
- Keywords            (type = Multiselect)

