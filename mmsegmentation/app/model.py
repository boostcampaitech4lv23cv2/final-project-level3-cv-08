import numpy as np
import torch
from mmseg.apis import inference_segmentor, init_segmentor
    
def get_model(config_path: str = "../configs/_sawol_/convnext/upernet_convnext_base_fp16_512x512_160k_ade20k_focal.py",
              checkpoint_path: str = "../work_dirs/upernet_convnext_base_fp16_512x512_160k_ade20k_focal/best_mIoU_iter_119000.pth"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = init_segmentor(config_path, checkpoint_path, device=device)
    return model

def predict_image(model, image_path: str) -> np.array:
    result = inference_segmentor(model, image_path)
    return result
