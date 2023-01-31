import io
import os
from pathlib import Path
import sys

import requests
from PIL import Image

import streamlit as st

sys.path.append('../')
from app.notion import find_car_number, update_car_status, get_config

st.set_page_config(layout="wide")

headers = get_config()['config']['headers']
car_number = st.text_input('차량번호')
phone_number = st.text_input('핸드폰 번호')
user_name = st.text_input('이름')
rental_select = st.selectbox("대여인가요?", ["대여", "반납"])

def main():
    st.title("Car Segmentation Model")
    uploaded_files = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        predict_image(uploaded_files)
        st.write("전송 완료")
    
    if st.button("결과 확인"):
        response = get_image(car_number)
        st.image(Image.open(io.BytesIO(response.content)))

@st.cache
def predict_image(uploaded_files):
    for uploaded_file in uploaded_files:
        uploaded_file.name = car_number + "/" + phone_number + "/" + user_name
        image_bytes = uploaded_file.getvalue()
        files = [
            ('files', (uploaded_file.name, image_bytes,
                    uploaded_file.type)),
        ]
        requests.post("http://localhost:8001/predict",files=files)
        

def authenticat_car(car_number) -> bool:
    car_numbers = find_car_number(car_number)
    return car_numbers != []
        
def authenticate_phone(phone_number) -> bool:
    return type(phone_number) == str and phone_number != ""

def authenticate_name(user_name) -> bool:
    return type(user_name) == str and user_name != ""

def get_image(car_number:str):
    response = requests.get(f"http://localhost:8001/images/{car_number}")
    return response

if authenticate_phone(phone_number) and authenticate_name(user_name) and authenticat_car(car_number):
    st.success('감사합니다!')
    update_car_status(car_number, rental_select, headers)
    main()
else:
    st.error('입력정보를 확인해주세요')