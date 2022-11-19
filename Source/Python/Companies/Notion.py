import requests
import json
import os
from notion_database.database import Database
from notion_database.page import Page
from notion_database.children import Children
from notion_database.request import Request

def init():

    global notion_companies_database_id
    notion_companies_database_id = os.getenv('NOTION_COMPANIES_DATABASE_ID')
    if notion_companies_database_id is None:
        raise ValueError("Please assign the target Notion patent database ID to the 'NOTION_COMPANIES_DATABASE_ID' environment variable.")

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
    print(f"Initialized Notion library: DB={notion_companies_database_id} TOKEN={notion_integration_token}")

def get_string(property):
    key = property['type']
    if key == 'title':
        title = property['title']
        if len(title) == 0: 
            return ''
        else:
            return title[0]['plain_text']
    if key == 'rich_text':
        rich_text = property['rich_text']
        if len(rich_text) == 0: 
            return ''
        else: 
            return rich_text[0]['plain_text']
    elif key == 'property_item':
        type = property['property_item']['type']
        if type == 'text':
            return property['property_item'][type]['text']['content']
        elif type == 'rich_text':
            return property['property_item'][type]
        else:
            return property['property_item'][type]
    else:
        return property[key]

def get_property(pageId, propertyId):
    url = f"https://api.notion.com/v1/pages/{pageId}/properties/{propertyId}"
    response = requests.get(url, headers=notion_header)
    data = json.loads(response.text)
    key = data['type']
    if key == 'property_item':
        type = data['property_item']['type']
        if type == 'text':
            result = data['property_item'][type]['text']['content']
        elif type == 'rich_text':
            result = data['property_item'][type]
        else:
            result = data['property_item'][type]
    else:
        result = data[key]
    return result


def get_all_companies():
    return get_all_items_in_database(database_id=notion_companies_database_id)

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
            # properties = {}
            # for property_name, property in page["properties"].items():
            #     property_value = get_property(page_id, property["id"])
            #     properties[property_name] = property_value
            items.append(page)
        has_more = database_query.result["has_more"]
    return items

def get_page_children(page_id):
    headers = {
        "accept": "application/json",
        "Notion-Version": "2022-06-28"
    }

    url = f"https://api.notion.com/v1/blocks/{page_id}/children?page_size=100"
    response = requests.get(url, headers=notion_header)
    response = json.loads(response.text)
    return response['results']


def update_icon(pageId, image):
    url = f'https://api.notion.com/v1/pages/{pageId}'

    payload = {
        "icon": {
            "type": "external",
            "external": {
                "url": image
            }
        },
    }

    response = requests.patch(url, headers=notion_header, json=payload)
    print(response)
