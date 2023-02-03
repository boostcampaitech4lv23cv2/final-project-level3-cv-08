import io
import sys
import requests
from PIL import Image
from pydantic import BaseModel, Field
from uuid import UUID, uuid4

import streamlit as st
from dotenv import dotenv_values
from notion_client import Client

sys.path.append('../')
from app.notion import createPage, update_car_status, get_database_pages

config = dotenv_values(".env")
notion_secret = config.get('NOTION_TOKEN')
car_database_id = config.get('CAR_DATABASE_ID')
serving_database_id = config.get('SERVING_DATABASE_ID')

notion = Client(auth=notion_secret)

class ImageId(BaseModel):
    id: UUID = Field(default_factory=uuid4)

detail = {0:"전면 좌측", 1: "전면 우측"}

st.set_page_config(layout="wide")

car_number = st.text_input('차량번호')
phone_number = st.text_input('핸드폰 번호')
user_name = st.text_input('이름')
rental_select = st.selectbox("대여인가요?", ["대여", "반납"])
rental_id = str(ImageId().id)

def main():
    st.title("Car Segmentation Model")
    uploaded_file_left = st.file_uploader("전면 좌측 사진", type=["jpg", "jpeg", "png"])
    uploaded_file_right = st.file_uploader("전면 우측 사진", type=["jpg", "jpeg", "png"])
    if uploaded_file_left and uploaded_file_right:
        uploaded_files = [uploaded_file_left, uploaded_file_right]
        data = predict_image(uploaded_files)
        st.write("전송 완료")
        save_notion(data)
    
    if st.button("결과 확인"):
        responses = get_image(car_number)
        for response in responses:
            st.image(Image.open(io.BytesIO(response.content)))

@st.cache
def predict_image(uploaded_files):
    data = None
    for idx, uploaded_file in enumerate(uploaded_files):
        uploaded_file.name = str(idx) + "/" + str(rental_id)
        image_bytes = uploaded_file.getvalue()
        files = [
            ('files', (uploaded_file.name, image_bytes,
                    uploaded_file.type)),
        ]
        temp = requests.post("http://localhost:8001/predict",files=files).json()
        
        if data == None:
            data = temp
        else:
            data['img_url'].append(temp['img_url'][0])
            data['pred_url'].append(temp['pred_url'][0])
            
        if temp['damage'] == "손상":
            data['damage'] = '손상'
            data['damage_idx'].append(detail[idx])

    return data

def authenticat_car(car_number) -> bool:
    car_numbers = get_database_pages(car_database_id, car_number)
    return car_numbers
        
def authenticate_phone(phone_number) -> bool:
    return type(phone_number) == str and phone_number != ""

def authenticate_name(user_name) -> bool:
    return type(user_name) == str and user_name != ""

def get_image(car_number:str):
    pages = get_database_pages(car_database_id, car_number)
    id = pages['properties']['대여 ID']['rich_text'][0]['plain_text']
    response = []
    for i in range(2):
        response.append(requests.get(f"https://storage.googleapis.com/rbc-bucket/{id}_pred_{i}.png"))
    return response

def save_notion(data:list):
    Data = {"databaseId": serving_database_id,
            "title": car_number,
            "phone_number": phone_number,
            "user_name": user_name,
            "damage": data['damage'],
            "damage_idx": data['damage_idx'],
            "ID": rental_id,
            "img_url": data['img_url'],
            "pred_url": data['pred_url'],
            }
            
    createPage(Data)
    update_car_status(car_number, rental_select, rental_id)

if authenticate_phone(phone_number) and authenticate_name(user_name) and authenticat_car(car_number):
    st.success('감사합니다!')
    main()
else:
    st.error('입력정보를 확인해주세요')