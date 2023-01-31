import io
import sys
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List

sys.path.append('../')
from app.db import read_log, write_log
from app.model import predict_image, damage_check
from app.config import get_setting
from app.notion import createPage, get_config

app = FastAPI()

class ImageId(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    image_id: UUID = Field(default_factory=uuid4)
    
# model과 config파일 가져옴
config = get_setting()
notion_cofig = get_config()
SAVE_PATH = config['SAVE_PATH']
data_info = config['data_info']
damage_info = config['damage']

@app.get("/")
def hello_world():
    return {"hello" : "world"}

@app.post("/predict", description="예측을 시작합니다")
async def make_pred(files: List[UploadFile] = File(...),
                    models = config['models']):
    for file in files:
        image_info = ImageId()
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image_array = np.array(image)

        image_name = str(image_info.image_id)
        pred_name = str(image_info.id)
        image_path = SAVE_PATH + image_name+".jpg"
        plt.imsave(image_path, image_array)
        pred_path = SAVE_PATH + pred_name + ".png"
        
        car_number, phone_number, user_name = file.filename.split("/")
        
        for model_key, model_val in models.items():
            pred_image = predict_image(model_val, image_path)
            plt.imsave(pred_path, pred_image[0])
            write_log(car_number, dict(image_info))
            Data = {"databaseId": notion_cofig['config']['databaseId'],
                    "title": car_number,
                    "phone_number": phone_number,
                    "user_name": user_name,
                    "damage": damage_info[damage_check(pred_image)],
                    }
            createPage(Data, notion_cofig['config']['headers'])

@app.get("/images/{car_number}")
def get_image(car_number: str):
    csv_data = read_log(car_number)
    iamge_info = csv_data
    return FileResponse(f"./DB/{iamge_info[data_info['image_id']]}.jpg")

# TODO: __main__ 파일로 옮김
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
