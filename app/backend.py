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
from app.db import write_log
from app.model import predict_image, damage_check
from app.config import get_setting

app = FastAPI()

class ImageId(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    damage: str = "정상"
    
# model과 config파일 가져옴
config = get_setting()
SAVE_PATH = config['SAVE_PATH']
damage_info = config['damage']

@app.post("/predict", response_model=ImageId)
async def make_pred(files: List[UploadFile] = File(...),
                    models = config['models']):
    for file in files:
        image_info = ImageId()
        image_bytes = await file.read()
        image = Image.open(io.BytesIO(image_bytes))
        image = image.convert("RGB")
        image_array = np.array(image)

        id = str(image_info.id)
        image_path = SAVE_PATH + id + ".jpg"
        plt.imsave(image_path, image_array)
        pred_path = SAVE_PATH + id + "_pred.png"
        
        car_number = file.filename
        for model_key, model_val in models.items():
            pred_image = predict_image(model_val, image_path)
            plt.imsave(pred_path, pred_image[0])
            write_log(car_number, dict(image_info))
            image_info.damage = damage_info[damage_check(pred_image)]
            return image_info
            
@app.get("/images/{rental_id}")
def get_image(rental_id: str):
    return FileResponse(f"./DB/{rental_id}.jpg")

@app.get("/pred_images/{rental_id}")
def get_image(rental_id: str):
    return FileResponse(f"./DB/{rental_id}_pred.png")


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8001)