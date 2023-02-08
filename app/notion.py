from dotenv import dotenv_values
from notion_client import Client

config = dotenv_values(".env")
notion_secret = config.get('NOTION_TOKEN')
car_database_id = config.get('CAR_DATABASE_ID')
serving_database_id = config.get('SERVING_DATABASE_ID')
notion = Client(auth=notion_secret)

# 데이터 베이스의 세부 내용 전송
def readDatabase(databaseId):
    data = notion.databases.query(databaseId)
    return data

def createPage(Data):
    newPageData = {
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
                "name": '원본이미지',
                "type": "external",
                "external": {
                    "url": f"http://localhost:8001/images/{Data['ID']}",
                }
                },
                {
                "name": "검사이미지",
                "type": "external",
                "external": {
                    "url": f"http://localhost:8001/pred_images/{Data['ID']}",
                }
                },
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
        '대여 ID': {
            "rich_text": [
                {
                    "text": {
                        "content": Data["ID"]
                    }
                }
            ]}
    }
    notion.pages.create(parent={'database_id': Data['databaseId']}, properties=newPageData)

def get_database_pages(database_id, page_name):
    pages = notion.databases.query(database_id=database_id)
    result = page_finder(pages, page_name)
    while pages['has_more'] and not result:
         pages = notion.databases.query(database_id=database_id, start_cursor=pages['next_cursor'])
    return result

def page_finder(pages, page_name):
    result_page = None
    for page in pages['results']:
        page_title = ""
        try:
            page_title = page['properties']['차량번호']['title'][0]['plain_text']
        except:
            pass
        if page_title == page_name:
            result_page = page
            break
    return result_page

def update_car_status(car_number: str, status: str, id:str):
    page_id = get_database_pages(car_database_id, page_name=car_number)['id']
    updateData = {
        '대여': {"status" : {'name': status}},
    }
    if status == "반납":
        updateData['대여 ID'] = {'rich_text': []}
    elif status == "대여":
        updateData['대여 ID'] = {'rich_text': [{'text': {'content': id}}]}
    
    notion.pages.update(page_id, properties=updateData)