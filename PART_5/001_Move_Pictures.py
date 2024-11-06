import os
import shutil
from tqdm import tqdm

def copy_pictures(source_dir, dest_dir):
    # Supported image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    # Ensure destination directory exists
    os.makedirs(dest_dir, exist_ok=True)

    print(f"Source directory: {source_dir}")
    print(f"Destination directory: {dest_dir}")

    # Walk through all directories in the source directory
    for root, dirs, files in os.walk(source_dir):
        print(f"Found directory: {root}")
        # Filter for image files
        image_files = [f for f in files if f.lower().endswith(image_extensions)]

        if image_files:
            print(f"Copying images from {root}")
            # Use tqdm to show progress bar for copying files
            for image_file in tqdm(image_files, desc=f"Copying from {root}"):
                source_file = os.path.join(root, image_file)
                dest_file = os.path.join(dest_dir, image_file)
                shutil.copy2(source_file, dest_file)

if __name__ == "__main__":
    source_directory = "IMAGE_DIRECTORIES"
    destination_directory = "ALL_PICTURES_TOGETHER"
    copy_pictures(source_directory, destination_directory)
