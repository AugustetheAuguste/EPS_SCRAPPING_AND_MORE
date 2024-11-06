import os
import shutil

def split_images_into_folders(source_folder, num_folders=5):
    # Create the subfolders if they don't already exist
    subfolders = [os.path.join(source_folder, f'folder_{i}') for i in range(1, num_folders + 1)]
    for subfolder in subfolders:
        os.makedirs(subfolder, exist_ok=True)

    # Get a list of all files in the source folder
    files = [f for f in os.listdir(source_folder) if os.path.isfile(os.path.join(source_folder, f))]

    # Calculate the number of files per folder
    files_per_folder = len(files) // num_folders
    remainder = len(files) % num_folders

    current_folder = 0
    count = 0

    for i, file in enumerate(files):
        if count >= files_per_folder + (1 if current_folder < remainder else 0):
            current_folder += 1
            count = 0
        
        src = os.path.join(source_folder, file)
        dest = os.path.join(subfolders[current_folder], file)
        shutil.move(src, dest)
        count += 1

    print(f"Successfully split {len(files)} images into {num_folders} folders.")

# Usage example
source_folder = 'ALL_PICTURES_TOGETHER'
split_images_into_folders(source_folder)
