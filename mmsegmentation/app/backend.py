import sys
import matplotlib.pyplot as plt
from PIL import Image
import io
import numpy as np

from fastapi import FastAPI, UploadFile, File
from fastapi.param_functions import Depends
from pydantic import BaseModel, Field
from uuid import UUID, uuid4
from typing import List, Union, Optional, Dict, Any

from mmseg.models.segmentors.encoder_decoder import EncoderDecoder
sys.path.append('../')
from app.model import get_model, predict_image

app = FastAPI()

class ImageId(BaseModel):
    car_number : str = "None"
    id: UUID = Field(default_factory=uuid4)
    image_id: UUID = Field(default_factory=uuid4)
    
images: List[ImageId] = []
SAVE_PATH = "./DB/"

@app.get("/")
def hello_world():
    return {"hello" : "world"}

@app.post("/predict", description="예측을 시작합니다")
async def make_pred(files: List[UploadFile] = File(...),
                    model: EncoderDecoder = Depends(get_model)):
    for file in files:
        image_info = ImageId()
        image_info.car_number = file.filename
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image_array = np.array(image)

        image_name = str(image_info.image_id)
        pred_name = str(image_info.id)
        
        plt.imsave(SAVE_PATH + image_name+".jpg", image_array)
        pred_image = predict_image(model, SAVE_PATH + image_name+".jpg")
        plt.imsave(SAVE_PATH + pred_name + ".jpg", pred_image[0])
        
        images.append(image_info)        
        

@app.get("/images")
def get_images():
    return images

@app.get("/images/{car_number}")
def get_image(car_number: str):
    for image in images:
        if image.car_number == car_number:
            return image

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)
