import os

import cv2 as cv
import numpy as np
import torch
from torchvision import transforms
from tqdm import tqdm

from config import device
from data_gen import data_transforms
from utils import ensure_folder

IMG_FOLDER = 'img_fusion/image_matting/data/alphamatting/input_lowres'
TRIMAP_FOLDERS = [
    'img_fusion/image_matting/data/alphamatting/trimap_lowres/Trimap1',
    'img_fusion/image_matting/data/alphamatting/trimap_lowres/Trimap2',
    'img_fusion/image_matting/data/alphamatting/trimap_lowres/Trimap3'
]
OUTPUT_FOLDERS = [
    'img_fusion/image_matting/images/alphamatting/output_lowres/Trimap1',
    'img_fusion/image_matting/images/alphamatting/output_lowres/Trimap2',
    'img_fusion/image_matting/images/alphamatting/output_lowres/Trimap3', 
]

if __name__ == '__main__':
    checkpoint = 'img_fusion/image_matting/BEST_checkpoint.tar'
    checkpoint = torch.load(checkpoint)
    model = checkpoint['model'].module
    model = model.to(device)
    model.eval()

    transformer = data_transforms['valid']

    ensure_folder('img_fusion/image_matting/images')
    ensure_folder('img_fusion/image_matting/images/alphamatting')
    ensure_folder(OUTPUT_FOLDERS[0])
    ensure_folder(OUTPUT_FOLDERS[1])
    ensure_folder(OUTPUT_FOLDERS[2])

    files = [f for f in os.listdir(IMG_FOLDER) if f.endswith('.png')]

    for file in tqdm(files):
        filename = os.path.join(IMG_FOLDER, file)
        img = cv.imread(filename)
        print(img.shape)
        h, w = img.shape[:2]

        x = torch.zeros((1, 4, h, w), dtype=torch.float)
        image = img[..., ::-1]  # RGB
        image = transforms.ToPILImage()(image)
        image = transformer(image)
        x[0:, 0:3, :, :] = image

        for i in range(3):
            filename = os.path.join(TRIMAP_FOLDERS[i], file)
            print('reading {}...'.format(filename))
            trimap = cv.imread(filename, 0)
            x[0:, 3, :, :] = torch.from_numpy(trimap.copy() / 255.)
            # print(torch.max(x[0:, 3, :, :]))
            # print(torch.min(x[0:, 3, :, :]))
            # print(torch.median(x[0:, 3, :, :]))

            # Move to GPU, if available
            x = x.type(torch.FloatTensor).to(device)

            with torch.no_grad():
                pred = model(x)

            pred = pred.cpu().numpy()
            pred = pred.reshape((h, w))

            pred[trimap == 0] = 0.0
            pred[trimap == 255] = 1.0

            out = (pred.copy() * 255).astype(np.uint8)

            filename = os.path.join(OUTPUT_FOLDERS[i], file)
            cv.imwrite(filename, out)
            print('wrote {}.'.format(filename))
