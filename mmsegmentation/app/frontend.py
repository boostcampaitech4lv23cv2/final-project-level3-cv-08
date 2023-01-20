import io
import os
from pathlib import Path
import sys

import requests
from PIL import Image

import streamlit as st

sys.path.append('../')
from app.confirm_button_hack import cache_on_button_press

st.set_page_config(layout="wide")

root_password = 'password'


def main():
    st.title("Car Segmentation Model")
    car_number = st.text_input("차량번호 입력", key="car_number")
    car_number_btn = st.button("확인")
    uploaded_file = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"])
        
    if uploaded_file:
        uploaded_file.name = car_number
        image_bytes = uploaded_file.getvalue()
        image = Image.open(io.BytesIO(image_bytes))

        st.image(image, caption='Uploaded Image')
        st.write("Segmenting...")
        st.write(car_number)
        files = [
            ('files', (uploaded_file.name, image_bytes,
                    uploaded_file.type))
        ]
        requests.post("http://localhost:8001/predict", files=files)
        
        response = get_images()
        st.write(response)
    
        


@cache_on_button_press('Authenticate')
def authenticate(password) -> bool:
    return password == root_password

def get_images():
    response = requests.get("http://localhost:8001/images")
    return response.json()


password = st.text_input('password', type="password")

if authenticate(password):
    st.success('You are authenticated!')
    main()
else:
    st.error('The password is invalid.')