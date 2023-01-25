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
from app.model import predict_image
from app.config import get_setting

app = FastAPI()

class ImageId(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    image_id: UUID = Field(default_factory=uuid4)
    damage: list = []

# model과 config파일 가져옴
config = get_setting()
SAVE_PATH = config['SAVE_PATH']
data_info = config['data_info']

@app.get("/")
def hello_world():
    return {"hello" : "world"}

@app.post("/predict", description="예측을 시작합니다")
async def make_pred(files: List[UploadFile] = File(...),
                    model = config['models']['separated']):
    for file in files:
        image_info = ImageId()
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image_array = np.array(image)

        image_name = str(image_info.image_id)
        pred_name = str(image_info.id)
        
        plt.imsave(SAVE_PATH + image_name+".jpg", image_array)
        pred_image = predict_image(model, SAVE_PATH + image_name+".jpg")
        plt.imsave(SAVE_PATH + pred_name + ".png", pred_image[0])
        write_log(file.filename, dict(image_info))
        

@app.get("/images/{car_number}")
def get_image(car_number: str):
    csv_data = read_log(car_number)
    iamge_info = csv_data
    return FileResponse(f"./DB/{iamge_info[data_info['id']]}.png")

# TODO: __main__ 파일로 옮김
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
