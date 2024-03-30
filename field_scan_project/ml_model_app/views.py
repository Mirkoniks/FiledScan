import cv2
# import numpy as np
import torch
from torch import Tensor
import tensorflow as tf
from ultralytics import YOLO
from django.shortcuts import render
from field_scan_project import settings

# Create your views here.
def image_model(image_path):
    # load a pretrained model (recommended for training)

    print(str(settings.BASE_DIR) + 'static\\wheat.pt')
    file = str(settings.BASE_DIR)+'\\static\\wheat.pt'
    mymodel = YOLO(file)


    # mymodel = tf.keras.models.load_model(r'C:\Users\Miro\Desktop\FieldScan\runs\classify\train25\weights\best.pt')

    # Load image
    img_path = str(settings.BASE_DIR)+'\\media\\' + image_path # Replace 'path_to_your_image.jpg' with the path to your image
    image = cv2.imread(img_path)

    # Resize image to match the model's input size
    input_size = (640, 640)  # Adjust this size based on your model's requirements
    resized_image = cv2.resize(image, input_size)

    # Convert resized image to PyTorch tensor
    image_tensor = torch.from_numpy(resized_image).permute(2, 0, 1).unsqueeze(0).float()

    # Perform inference
    detection_results = mymodel(image_tensor)

    # Process the detection results
    # Depending on your model's output, you may need to extract confidence scores
    # and other information from the detection results

    # for det in detection_results:
    #     print(det)

    # print(detection_results[0].names)

    # print(list(detection_results[0].probs.top5conf))
    return detection_results[0].probs.top5conf

