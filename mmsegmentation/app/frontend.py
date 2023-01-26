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


def main():
    st.title("Car Segmentation Model")
    uploaded_files = st.file_uploader("Choose an image", type=["jpg", "jpeg", "png"], accept_multiple_files=True)
    if uploaded_files:
        for uploaded_file in uploaded_files:
            uploaded_file.name = car_number
            image_bytes = uploaded_file.getvalue()
            image = Image.open(io.BytesIO(image_bytes))

            st.image(image, caption='Uploaded Image')
            st.write("Segmenting...")
            files = [
                ('files', (uploaded_file.name, image_bytes,
                        uploaded_file.type))
            ]
            requests.post("http://localhost:8001/predict", files=files)
    
    if st.button("결과 확인"):
        response = get_image(car_number)
        st.image(Image.open(io.BytesIO(response.content)))


@cache_on_button_press('Authenticate')
def authenticate(car_number) -> bool:
    return type(car_number) == str

def get_images():
    response = requests.get("http://localhost:8001/images")
    return response.json()

def get_image(car_number:str):
    response = requests.get(f"http://localhost:8001/images/{car_number}")
    return response

car_number = st.text_input('Car number')

if authenticate(car_number):
    st.success('You are authenticated!')
    main()
else:
    st.error('The car number is invalid.')