import os
import sys
import numpy as np
import cv2

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List

sys.path.append('../')
from app.model import predict_image, damage_check
from app.config import get_setting
from app.gcs import upload_image

app = FastAPI()

class ImageId(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    damage: str = "정상"
    damage_idx: list = []
    img_url: list = []
    pred_url: list = []
    
# model과 config파일 가져옴
config = get_setting()
SAVE_PATH = config['SAVE_PATH']
damage_info = config['damage']
models = config['models']

@app.post("/predict", response_model=ImageId)
async def make_pred(files: List[UploadFile] = File(...)):
    for file in files:
        image_info = ImageId()
        # id = str(image_info.id)
        idx, id = file.filename.split("/")
        image_info.id = id
        image_name = id + f"_{idx}.jpg"
        pred_name = id + f"_pred_{idx}.png"
        image_path = SAVE_PATH + image_name
        pred_path = SAVE_PATH + pred_name
        
        image_bytes = await file.read()       
        img_array = np.frombuffer(image_bytes, np.uint8)
        img = cv2.imdecode(img_array, cv2.IMREAD_UNCHANGED)
        cv2.imwrite(image_path, img)
        
        image_info.img_url.append(upload_image(image_name))
        
        for model_key, model_val in models.items():
            pred_image = predict_image(model_val, image_path)
            pred_image = np.array(pred_image[0])
            img[pred_image == 1] = [0,0,0]
            cv2.imwrite(pred_path, img)
            image_info.pred_url.append(upload_image(pred_name))
            image_info.damage = damage_info[damage_check(pred_image)]
            
            os.remove(image_path)
            os.remove(pred_path)
            return image_info

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
