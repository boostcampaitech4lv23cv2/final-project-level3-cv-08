import numpy as np
import torch
from mmseg.apis import inference_segmentor, init_segmentor

def get_model(config_path: str, checkpoint_path: str):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = init_segmentor(config_path, checkpoint_path, device=device)
    return model

def predict_image(model, image_path: str) -> np.array:
    result = inference_segmentor(model, image_path)
    return result

def damage_check(pred_image: np.array) -> bool:
    return np.any(pred_image >= 1)