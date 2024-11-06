from mtcnn import MTCNN
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import torch
from transformers import ResNetForImageClassification
from torchvision import transforms

import sys
import codecs


# Set encoding to UTF-8 for all standard I/O operations
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())


# Function to detect and extract all faces from a given image
def extract_faces(pixels, required_size=(224, 224)):
    # Create the detector, using default weights
    detector = MTCNN()
    # Detect faces in the image
    results = detector.detect_faces(pixels)
    
    faces = []

    # Use tqdm for progress bar
    for result in tqdm(results, desc="Processing Faces"):
        # Extract the bounding box from the detected face
        x1, y1, width, height = result['box']
        x2, y2 = x1 + width, y1 + height
        
        # Extract the face
        face = pixels[y1:y2, x1:x2]
        
        # Resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = np.asarray(image)
        
        # Append face array to faces list
        faces.append(face_array)
    
    return faces

# Function to classify faces
def classify_faces(faces):
    # Load the state dictionary
    model_path = 'final_model_resnet_50.pt'
    state_dict = torch.load(model_path, map_location=torch.device('cpu'))

    # Initialize the ResNet model using transformers
    model = ResNetForImageClassification.from_pretrained("microsoft/resnet-50")
    # Modify the classifier layer to match the training script
    model.classifier[1] = torch.nn.Linear(in_features=2048, out_features=2, bias=True)

    # Load the state dictionary into the model
    model.load_state_dict(state_dict)
    model.eval()

    # Define the preprocessing steps
    preprocess = transforms.Compose([
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
    ])

    predictions = []
    for i, face in enumerate(faces):
        # Preprocess the face
        face_image = Image.fromarray(face)
        input_tensor = preprocess(face_image)
        input_batch = input_tensor.unsqueeze(0)

        # Make predictions
        with torch.no_grad():
            output = model(input_batch)
        
        # Interpret the output (assuming binary classification)
        _, predicted_class = torch.max(output.logits, 1)
        predictions.append(predicted_class.item())
        print(f'Face {i+1} Predicted Class: {predicted_class.item()}')

    return predictions

# Example usage:
image_path = 'withought_real.jpeg'
pixels = plt.imread(image_path)
faces = extract_faces(pixels)
classify_faces(faces)
