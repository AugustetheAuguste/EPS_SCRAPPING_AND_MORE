from mtcnn import MTCNN
from PIL import Image
import numpy as np
import torch
from transformers import ResNetForImageClassification
from torchvision import transforms
import matplotlib.pyplot as plt
import mediapipe as mp
import tensorflow as tf


# Pre-initialize the MTCNN detector and make sure TensorFlow uses CPU
with tf.device('/CPU:0'):
    detector = MTCNN()


class ImageWithFaces:
    def __init__(self, image_path):
        self.image_path = image_path
        self.faces = []

def init_resnet():
    model_path = 'final_model_resnet_50.pt'
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")
    model.classifier[1] = torch.nn.Linear(in_features=2048, out_features=2, bias=True)
    model.load_state_dict(state_dict)
    model.eval()
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])
    return model, preprocess


def extract_faces_mtcnn(image_path, required_size=(224, 224)):
    with tf.device('/CPU:0'):  # Force MTCNN to use the CPU
        detector = MTCNN()
        image = Image.open(image_path)
        image = image.convert('RGB')
        pixels = np.asarray(image)

        results = detector.detect_faces(pixels)
        img_faces = ImageWithFaces(image_path)

        for result in results:
            x1, y1, width, height = result['box']
            x2, y2 = x1 + width, y1 + height

            x1, y1, x2, y2 = max(0, x1), max(0, y1), max(0, x2), max(0, y2)

            face = pixels[y1:y2, x1:x2]
            face_image = Image.fromarray(face)
            face_image = face_image.resize(required_size)
            face_array = np.asarray(face_image)
            img_faces.faces.append(face_array)

    return img_faces

def extract_faces_mediapipe(image_paths, required_size=(224, 224)):
    mp_face_detection = mp.solutions.face_detection
    images = []
    
    with mp_face_detection.FaceDetection(model_selection=1, min_detection_confidence=0.5) as face_detection:
        for image_path in image_paths:
            # Load image using PIL to ensure it's RGB
            image = Image.open(image_path).convert('RGB')
            pixels = np.asarray(image)

            results = face_detection.process(pixels)
            img_faces = ImageWithFaces(image_path)
            
            if results.detections:
                for detection in results.detections:
                    bbox = detection.location_data.relative_bounding_box
                    ih, iw, _ = pixels.shape
                    x1, y1 = int(bbox.xmin * iw), int(bbox.ymin * ih)
                    x2, y2 = x1 + int(bbox.width * iw), y1 + int(bbox.height * ih)
                    
                    # Correct negative coordinates
                    x1, y1, x2, y2 = max(0, x1), max(0, y1), max(0, x2), max(0, y2)
                    
                    face = pixels[y1:y2, x1:x2]
                    image = Image.fromarray(face)
                    image = image.resize(required_size)
                    face_array = np.asarray(image)
                    img_faces.faces.append(face_array)
            
            images.append(img_faces)
    return images


def classify_faces(images, model, preprocess):
    for img_faces in images:
        predictions = []
        for face in img_faces.faces:
            face_image = Image.fromarray(face)
            input_tensor = preprocess(face_image)
            input_batch = input_tensor.unsqueeze(0)
            with torch.no_grad():
                output = model(input_batch)
            _, predicted_class = torch.max(output.logits, 1)
            predictions.append(predicted_class.item())
        img_faces.predictions = predictions
