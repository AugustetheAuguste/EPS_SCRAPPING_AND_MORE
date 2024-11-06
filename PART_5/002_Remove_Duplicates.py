import os
import hashlib
from tqdm import tqdm

def file_hash(file_path):
    """Generate a hash for a file using SHA-256."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def remove_duplicates(source_dir):
    # Supported image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    # Dictionary to store file hashes and their paths
    hashes = {}
    duplicates_count = 0

    print(f"Source directory: {source_dir}")

    # Walk through all directories in the source directory
    for root, dirs, files in os.walk(source_dir):
        print(f"Checking directory: {root}")
        # Filter for image files
        image_files = [f for f in files if f.lower().endswith(image_extensions)]

        if image_files:
            # Use tqdm to show progress bar for checking files
            for image_file in tqdm(image_files, desc=f"Processing {root}"):
                file_path = os.path.join(root, image_file)
                file_hash_value = file_hash(file_path)

                if file_hash_value in hashes:
                    # Duplicate found, remove the file
                    os.remove(file_path)
                    duplicates_count += 1
                else:
                    # Store hash and file path
                    hashes[file_hash_value] = file_path

    print(f"Total duplicates deleted: {duplicates_count}")

if __name__ == "__main__":
    source_directory = "ALL_PICTURES_TOGETHER"
    remove_duplicates(source_directory)
