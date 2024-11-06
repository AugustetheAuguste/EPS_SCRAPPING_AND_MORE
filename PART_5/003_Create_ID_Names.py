import os
import hashlib
import uuid
from tqdm import tqdm

def file_hash(file_path):
    """Generate a hash for a file using SHA-256."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hasher.update(chunk)
    return hasher.hexdigest()

def assign_unique_ids(source_dir):
    # Supported image file extensions
    image_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp', '.tiff')

    # Dictionary to store file hashes and their paths
    hashes = {}
    duplicates_count = 0

    print(f"Source directory: {source_dir}")

    # Walk through all directories in the source directory
    for root, dirs, files in os.walk(source_dir):
        print(f"Processing directory: {root}")
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
                    # Generate a unique ID for the file
                    unique_id = str(uuid.uuid4())
                    # Get the file extension
                    file_extension = os.path.splitext(file_path)[1]
                    # Generate new file name with unique ID
                    new_file_name = unique_id + file_extension
                    new_file_path = os.path.join(root, new_file_name)
                    # Rename the file
                    os.rename(file_path, new_file_path)

    print(f"Total duplicates deleted: {duplicates_count}")

if __name__ == "__main__":
    source_directory = "ALL_PICTURES_TOGETHER"
    assign_unique_ids(source_directory)
