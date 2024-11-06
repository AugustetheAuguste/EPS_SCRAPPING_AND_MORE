from mtcnn import MTCNN
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

import sys
import codecs

# Set encoding to UTF-8 for all standard I/O operations
sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())
sys.stdin = codecs.getreader("utf-8")(sys.stdin.detach())


# Function to detect and extract all faces from a given image
def extract_faces(filename, required_size=(224, 224)):
    # Load image from file
    pixels = plt.imread(filename)
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
    
    # Print the number of detected faces
    print(f"Number of faces detected: {len(faces)}")
    
    # Print faces one by one
    for i, face in enumerate(faces):
        plt.imshow(face)
        plt.title(f"Face {i+1}")
        plt.show()
    
    return faces

# Example usage:
try:
    faces = extract_faces('withought_real.jpeg')
except UnicodeEncodeError as e:
    print(f"Encoding error: {e}")

