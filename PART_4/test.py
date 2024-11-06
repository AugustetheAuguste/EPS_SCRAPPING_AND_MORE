# test.py
# test.py
import os
import zipfile
import shutil
import time
from utils import extract_faces_mediapipe, extract_faces_mtcnn, classify_faces, init_resnet
from tqdm import tqdm
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(message)s')


def move_images(images, model, preprocess, class_1_dir, class_2_dir):
    logging.info("Classifying faces...")
    start_time = time.time()
    classify_faces(images, model, preprocess)
    logging.info(f"Classification completed in {time.time() - start_time:.2f} seconds\n")

    logging.info("Moving images based on predictions...")
    start_time = time.time()
    for img_faces in tqdm(images, desc="Moving images"):
        if os.path.exists(img_faces.image_path):
            target_dir = class_1_dir if 1 in img_faces.predictions else class_2_dir
            shutil.move(img_faces.image_path, os.path.join(target_dir, os.path.basename(img_faces.image_path)))
        else:
            logging.warning(f"File {img_faces.image_path} not found. Skipping.")
    logging.info(f"Moving completed in {time.time() - start_time:.2f} seconds\n")


def process_zip(zip_path):
    logging.info("Initializing ResNet model...")
    start_time = time.time()
    model, preprocess = init_resnet()
    logging.info(f"Model initialized in {time.time() - start_time:.2f} seconds\n")

    if not os.path.exists(zip_path):
        logging.error(f'File not found: {zip_path}')
        return

    logging.info("Extracting ZIP file contents...")
    start_time = time.time()
    extract_dir = 'extracted'
    if os.path.exists(extract_dir):
        shutil.rmtree(extract_dir)
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_dir)
    logging.info(f"Extraction completed in {time.time() - start_time:.2f} seconds\n")

    class_1_dir = 'class_1'
    class_2_dir = 'class_2'
    for dir_name in [class_1_dir, class_2_dir]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
        os.makedirs(dir_name, exist_ok=True)

    image_files = [os.path.join(extract_dir, f) for f in os.listdir(extract_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]

    logging.info("Detecting faces with MediaPipe...")
    start_time = time.time()
    images = extract_faces_mediapipe(tqdm(image_files, desc="Processing with MediaPipe"))
    logging.info(f"Face detection with MediaPipe completed in {time.time() - start_time:.2f} seconds\n")

    move_images(images, model, preprocess, class_1_dir, class_2_dir)

    class_1_images = [os.path.join(class_1_dir, f) for f in os.listdir(class_1_dir) if f.lower().endswith(('png', 'jpg', 'jpeg'))]
    processed_images = []

    logging.info("Detecting faces with MTCNN (second pass)...")
    start_time = time.time()
    for img_path in tqdm(class_1_images, desc="Processing with MTCNN"):
        if not os.path.exists(img_path):
            logging.warning(f"File {img_path} not found. Skipping.")
            continue

        img_faces = extract_faces_mtcnn(img_path)
        classify_faces([img_faces], model, preprocess)
        processed_images.append(img_faces)
    logging.info(f"Face detection and classification with MTCNN completed in {time.time() - start_time:.2f} seconds\n")

    move_images(processed_images, model, preprocess, class_1_dir, class_2_dir)

    logging.info("Creating ZIP files...")
    start_time = time.time()
    shutil.make_archive('class_1', 'zip', class_1_dir)
    shutil.make_archive('class_2', 'zip', class_2_dir)
    logging.info(f"ZIP files created in {time.time() - start_time:.2f} seconds\n")

    logging.info("Processing completed. Check the current directory for 'class_1.zip' and 'class_2.zip'")


if __name__ == "__main__":
    zip_path = r"wetransfer_photo-passation_2024-04-25_1909.zip"
    process_zip(zip_path)
