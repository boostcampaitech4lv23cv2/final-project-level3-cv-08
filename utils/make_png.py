import os
import cv2
import numpy as np
import json
from tqdm import tqdm
from skimage.draw import polygon2mask
import shutil
import argparse

def main(args):
    pass_cnt = 0

    json_dir = args.json_dir
    img_dir = args.img_dir
    file_names = os.listdir(json_dir)
    output_ann_dir = args.output_ann_dir
    output_img_dir = args.output_img_dir
    os.makedirs(output_ann_dir, exist_ok=True)
    os.makedirs(output_img_dir, exist_ok=True)

    if args.damage_type == "Whole":
        # Whole type
        damage_type = {'Scratched':1, 'Crushed':2, 'Breakage':3, 'Separated':4} # num : priority

        for file_name in tqdm(file_names):
            with open(os.path.join(json_dir, file_name)) as f:
                data = json.load(f)

            height, width = data['images']['height'], data['images']['width']
            result_array = np.zeros((height, width))
            n = len(data['annotations'])
            
            for i in range(n):
                polygons = data['annotations'][i]['segmentation']
                type = damage_type[data['annotations'][i]['damage']]
                for j in range(len(polygons)):
                    for k in range(len(polygons[j])):
                        tmp = np.array(polygons[j][k]).squeeze()
                        poly = [[p[1], p[0]] for p in tmp]
                        mask = polygon2mask((height,width), poly) * type
                        if k == 0:
                            result_array = np.maximum(result_array, mask)
                        else:
                            result_array[mask == 1] = 0
                        
                        
            cv2.imwrite(os.path.join(output_ann_dir, file_name.split('.')[0]+'.png'), result_array.astype(np.uint8))

    elif args.damage_type in ['Scratched', 'Crushed', 'Breakage', 'Separated']:
        damage_type = args.damage_type

        for file_name in tqdm(file_names):
            with open(os.path.join(json_dir, file_name)) as f:
                data = json.load(f)

            height, width = data['images']['height'], data['images']['width']
            result_array = np.zeros((height, width))
            n = len(data['annotations'])
            save_flag = False
            for i in range(n):
                polygons = data['annotations'][i]['segmentation']
                type = data['annotations'][i]['damage']
                if type != damage_type:
                    continue
                if not save_flag:
                    save_flag = True
                for j in range(len(polygons)):
                    for k in range(len(polygons[j])):
                        tmp = np.array(polygons[j][k]).squeeze()
                        poly = [[p[1], p[0]] for p in tmp]
                        mask = polygon2mask((height,width), poly)
                        if k == 0:
                            result_array = np.maximum(result_array, mask)
                        else:
                            result_array[mask == 1] = 0
            if save_flag:
                name = file_name.split('.')[0]
                try:
                    shutil.copy(os.path.join(img_dir, name+'.jpg'), output_img_dir)
                    cv2.imwrite(os.path.join(output_ann_dir, name+'.png'), result_array.astype(np.uint8))
                except:
                    pass_cnt += 1
        print(f"pass_cnt: {pass_cnt}")
    
if __name__ == "__main__":
    parse = argparse.ArgumentParser()
    parse.add_argument("--json_dir", default='../../RBCs/data/train/label/damage')
    parse.add_argument("--img_dir", default='../../RBCs/data/train/img/damage')
    parse.add_argument("--output_ann_dir", default='../../RBCs/data/train/ann_dir/train/')
    parse.add_argument("--output_img_dir", default='../../RBCs/data/train/img_dir/train/')
    parse.add_argument("--damage_type", default='Whole')

    args = parse.parse_args()
    main(args)