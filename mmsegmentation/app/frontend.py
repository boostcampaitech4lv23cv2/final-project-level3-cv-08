import io
import sys
import requests
from PIL import Image

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

st.set_page_config(layout="wide")

car_number = st.text_input('차량번호')
phone_number = st.text_input('핸드폰 번호')
user_name = st.text_input('이름')
rental_select = st.selectbox("대여인가요?", ["대여", "반납"])

def main():
    st.title("Car Segmentation Model")
    uploaded_files = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        data = predict_image(uploaded_files)
        st.write("전송 완료")
        save_notion(data)
    
    if st.button("결과 확인"):
        response = get_image(car_number)
        st.image(Image.open(io.BytesIO(response.content)))

@st.cache
def predict_image(uploaded_files):
    for uploaded_file in uploaded_files:
        uploaded_file.name = car_number
        image_bytes = uploaded_file.getvalue()
        files = [
            ('files', (uploaded_file.name, image_bytes,
                    uploaded_file.type)),
        ]
        data = requests.post("http://localhost:8001/predict",files=files)
        return data.json()        

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
    response = requests.get(f"http://localhost:8001/pred_images/{id}")
    return response

def save_notion(data:dict):
    Data = {"databaseId": serving_database_id,
            "title": car_number,
            "phone_number": phone_number,
            "user_name": user_name,
            "damage": data['damage'],
            "ID": data['id']
            }
            
    createPage(Data)
    update_car_status(car_number, rental_select, data['id'])

if authenticate_phone(phone_number) and authenticate_name(user_name) and authenticat_car(car_number):
    st.success('감사합니다!')
    main()
else:
    st.error('입력정보를 확인해주세요')