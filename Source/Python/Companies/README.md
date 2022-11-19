# EtAlii.Notion

Simple script to add images from an URL into a Notion database page.

Before starting, make sure all required libraries are installed using pip.

for example:

```python
pip install requests
pip install notion_database
pip install urllib
```

Also required are the following environment variables:

- NOTION_INTEGRATION_TOKEN
- NOTION_PATENT_DATABASE_ID
- NOTION_PATENT_SEARCHES

With Powershell these can be set using:

```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_INTEGRATION_TOKEN", "YOUR_NOTION_INTEGRATION_TOKEN")
[System.Environment]::SetEnvironmentVariable("NOTION_COMPANIES_DATABASE_ID", "YOUR_NOTION_COMPANIES_DATABASE_ID")
```

If you want to make a persist an environment variable for the current user profile:

```powershell
[System.Environment]::SetEnvironmentVariable("NOTION_COMPANIES_DATABASE_ID", "YOUR_NOTION_COMPANIES_DATABASE_ID", [System.EnvironmentVariableTarget]::User)
```

The target database should have the following columns:

- Id                  (Type = Title)
- Url                 (type = Url)
- Image               (type = Text)

