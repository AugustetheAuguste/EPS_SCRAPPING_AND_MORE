# callbacks.py
from dash import html, Output, Input, State
import os
import zipfile
import shutil
from utils import extract_faces_mediapipe, extract_faces_retinaface, classify_faces, init_resnet
import matplotlib.pyplot as plt

def register_callbacks(app):
    @app.callback(
        Output('output', 'children'),
        [Input('process-button', 'n_clicks')],
        [State('upload-zip', 'isCompleted'), State('upload-zip', 'fileNames')]
    )
    def process_zip(n_clicks, is_completed, file_names):
        if n_clicks == 0 or not is_completed or not file_names:
            return 'No files uploaded or process button not clicked'

        model, preprocess = init_resnet()

        session_folder = os.path.join('uploads', os.listdir('uploads')[0])
        zip_filename = file_names[0]
        zip_path = os.path.join(session_folder, zip_filename)

        if not os.path.exists(zip_path):
            return f'File not found: {zip_path}'

        extract_dir = 'extracted'
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_dir)

        class_1_dir = 'class_1'
        class_2_dir = 'class_2'
        os.makedirs(class_1_dir, exist_ok=True)
        os.makedirs(class_2_dir, exist_ok=True)

        image_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir)]

        # First pass with MediaPipe
        images = extract_faces_mediapipe(image_files)
        classify_faces(images, model, preprocess)

        # Filter images with class 1 prediction for a second pass
        class_1_images = [img_faces.image_path for img_faces in images if 1 in img_faces.predictions]
        
        # Second pass with RetinaFace for images with class 1 prediction
        updated_images = []
        for img_path in class_1_images:
            img_faces = extract_faces_retinaface(img_path)
            classify_faces([img_faces], model, preprocess)
            updated_images.append(img_faces)

        # Move images based on final predictions
        for img_faces in images + updated_images:
            if 1 in img_faces.predictions:
                shutil.move(img_faces.image_path, os.path.join(class_1_dir, os.path.basename(img_faces.image_path)))
            else:
                shutil.move(img_faces.image_path, os.path.join(class_2_dir, os.path.basename(img_faces.image_path)))

        shutil.make_archive('class_1', 'zip', class_1_dir)
        shutil.make_archive('class_2', 'zip', class_2_dir)

        return html.Div([
            html.A("Download Class 1 Images", href=f"/downloads/class_1.zip", className="btn btn-secondary mx-2"),
            html.A("Download Class 2 Images", href=f"/downloads/class_2.zip", className="btn btn-secondary mx-2")
        ])
