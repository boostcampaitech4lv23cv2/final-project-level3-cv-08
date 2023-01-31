import yaml
import requests, json


def readDatabase(databaseId, headers):
    
    readUrl = f"https://api.notion.com/v1/databases/{databaseId}/query"

    res = requests.post(readUrl, headers=headers)

    data = res.json()
    with open("./db.json", "w", encoding="utf8") as f:
        json.dump(data, f, ensure_ascii=False)
        
    return data

def createPage(Data, headers):
    createUrl = 'https://api.notion.com/v1/pages'
    newPageData = {
        "parent": { "database_id": Data['databaseId'] },
        "properties": {
            "차량번호": {
                "title": [
                    {
                        "text": {
                            "content": Data["title"]
                        }
                    }
                ]
            },
            "파일과 미디어": {
                "files": [
                    {
                    "name": Data['title'],
                    "type": "external",
                    "external": {
                        "url": f"http://localhost:8001/images/{Data['title']}",
                    }
                    }
                ]
            },
            '전화번호': {'phone_number': Data['phone_number']},
            "대여자 성함": {
                "rich_text": [
                    {
                        "text": {
                            "content": Data["user_name"]
                        }
                    }
                ]
            },
            '손상': {'status': {'name': Data['damage']}},
        }
    }
    newPageData = newPageData
    data = json.dumps(newPageData)
    requests.request("POST", createUrl, headers=headers, data=data)

def get_config(config_path: str = "notion.yaml"):
    with open(config_path) as f:
        config = yaml.load(f, Loader=yaml.FullLoader)
    return config

def get_notion_car_database():
    config = get_config()
    return readDatabase(config['config']['CarDatabaseId'], config['config']['headers'])['results']

def find_car_number(car_number: str):
    data = get_notion_car_database()
    return [i for i in data if i['properties']['차량번호']['title'][0]['plain_text'] == car_number]

def update_car_status(car_number: str, status: str, headers):
    data = find_car_number(car_number)[0]
    updateUrl = f"https://api.notion.com/v1/pages/{data['id']}"
    updateData = {
        'properties': {
            '대여': {
                "status" : {'name': status}
            }
        }
    }
    data = json.dumps(updateData)
    requests.patch(updateUrl, headers=headers, data=data)