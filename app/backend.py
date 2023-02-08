import os
import sys
import numpy as np
import cv2

from dotenv import dotenv_values
from starlette.middleware.cors import CORSMiddleware

from fastapi import FastAPI, File, Form
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List

sys.path.append('../')
from app.model import predict_image, damage_check
from app.config import get_setting
from app.gcs import upload_image
from notion import update_car_status, createPage

app = FastAPI()

origins = [
    'http://localhost:3000',
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

class RentalId(BaseModel):
    id: UUID = Field(default_factory=uuid4)

class ResultOfUpload(BaseModel):
    pred_url: list = []

# # model과 config파일 가져옴
config = get_setting()
SAVE_PATH = config['SAVE_PATH']
models = config['models']

config = dotenv_values(".env")
serving_database_id = config.get('SERVING_DATABASE_ID')

detail = {0:"전면 좌측", 1: "전면 우측", 2: "후면 좌측", 3:"후면 우측"}

@app.post("/upload", response_model=ResultOfUpload)
async def receiveFile(
    carFrontImg: bytes = File(...), 
    carBackImg: bytes = File(...),
    carLeftImg: bytes = File(...),
    carRightImg: bytes = File(...),
    userName: str = Form(...),
    carNum: str = Form(...),
    userPhone: str = Form(...),
    userRent: str = Form(...)):
    
    id = str(RentalId().id)
    img_url = []
    pred_url = []
    damage_idx = []
    damage = "정상"
    for idx, img in enumerate([carFrontImg, carBackImg, carLeftImg, carRightImg]):
        image_name = id + f"_{idx}.jpg"
        pred_name = id + f"_pred_{idx}.png"
        image_path = SAVE_PATH + image_name
        pred_path = SAVE_PATH + pred_name
        
        img_array = np.frombuffer(img, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        cv2.imwrite(image_path, img)
        
        img_url.append(upload_image(image_name))
        
        for model_key, model_val in models.items():
            pred_image = predict_image(model_val, image_path)
            pred_image = np.array(pred_image[0])
            img[pred_image == 1] = [225,0,0]
            cv2.imwrite(pred_path, img)
            pred_url.append(upload_image(pred_name))
            if damage_check(pred_image):
                damage_idx.append(detail[idx])
                damage = "손상"
            
        os.remove(image_path)
        os.remove(pred_path)
    
    save_notion(serving_database_id, id, carNum, userPhone, userName,damage, userRent, damage_idx, img_url, pred_url)
    res = ResultOfUpload()
    res.pred_url = pred_url
    return res

def save_notion(databaseId:str,
                      ID: str, 
                      title: str,
                      phone_number: str,
                      user_name: str,
                      damage: str,
                      userRent: str,
                      damage_idx: list,
                      img_url: list, 
                      pred_url: list):
            
    createPage( databaseId,
                ID, 
                title,
                phone_number,
                user_name,
                damage,
                damage_idx,
                img_url, 
                pred_url)
    update_car_status(title, userRent, ID)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=30002)
