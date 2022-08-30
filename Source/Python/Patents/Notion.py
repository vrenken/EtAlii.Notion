import requests
import json
import os
from notion_database.database import Database


def init():

    global notion_patent_database_id
    notion_patent_database_id = os.getenv('NOTION_PATENT_DATABASE_ID')
    if notion_patent_database_id is None:
        raise ValueError("Please assign the target Notion patent database ID to the 'NOTION_PATENT_DATABASE_ID' environment variable.")

    global notion_integration_token
    notion_integration_token = os.getenv('NOTION_INTEGRATION_TOKEN')
    if notion_integration_token is None:
        raise ValueError("Please assign your Notion integration token to the 'NOTION_INTEGRATION_TOKEN' environment variable.")

    global notion_header
    notion_header = {
        "Authorization": f"Bearer {notion_integration_token}",
        "Accept": "application/json",
        "Notion-Version": "2022-06-28"
    }
    print("Initialized Notion library")

def get_property(pageId, propertyId):
    url = f"https://api.notion.com/v1/pages/{pageId}/properties/{propertyId}"
    response = requests.get(url, headers=notion_header)
    data = json.loads(response.text)
    key = data['type']
    if key == 'property_item':
        type = data['results'][0]['type']
        result = data['results'][0][type]['text']['content']
    else:
        result = data[key]
    return result


def get_all_items_in_database(database_id):
    items = list()
    has_more = True
    first_request = True
    database_query = Database(integrations_token=notion_integration_token)
    while has_more:
        if first_request:
            database_query.find_all_page(database_id=database_id)
        else:
            database_query.find_all_page(database_id=database_id, start_cursor=database_query.result["next_cursor"])
            first_request = False
        for page in database_query.result["results"]:
            page_id = page["id"]
            properties = {}
            for property_name, property in page["properties"].items():
                property_value = get_property(page_id, property["id"])
                properties[property_name] = property_value
            items.append(properties)
        has_more = database_query.result["has_more"]
    return items


def has_patent(patent):
    url = f"https://api.notion.com/v1/databases/{notion_patent_database_id}/query"
    payload = {
        "filter": {
            "property": "Id",
            "title": {
                "equals": patent["Id"]
                }
            }
        }
    response = requests.post(url, headers=notion_header, json=payload)
    data = json.loads(response.text)
    has_patent = len(data['results']) > 0
    if has_patent:
        print(f"Checking patent from Notion: {patent['Id']}: Found")
    else:
        print(f"Checking patent from Notion: {patent['Id']}: Not found")

    return has_patent


def add_patent(patent):
    url = f'https://api.notion.com/v1/pages'
    payload = {
        "parent": {
            "type": "database_id",
            "database_id": notion_patent_database_id
        },
        "properties": {
            "Id": {
                "title": [
                    {
                        "text": {
                            "content": patent['Id']
                        }
                    }
                ]
            },
            "Title": {
                "rich_text": [
                    {
                        "text": {
                            "content": patent['Title']
                        }
                    }
                ]
            },
            "Inventor": {
                "rich_text": [
                    {
                        "text": {
                            "content": patent['Inventor']
                        }
                    }
                ]
            },
            "Assignee": {
                "rich_text": [
                    {
                        "text": {
                            "content": patent['Assignee']
                        }
                    }
                ]
            },
            "Filing date": {
                "date": {"start": patent['Filing date']}
            },
            "Publication date": {
                "date": {"start": patent['Publication date']}
            },
            "Url": {
                "url": patent['Url']
            },
        }
    }
    response = requests.post(url, headers=notion_header, json=payload)

    print(f"Added patent to Notion: {patent['Id']}")

    return response.json()
