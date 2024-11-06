import os
import hashlib
import shutil  # Import shutil for deleting non-empty directories

def sanitize_filename(name):
    """Sanitize strings to be used as filenames by hashing."""
    return hashlib.md5(name.encode()).hexdigest()

def delete_directories(root_dir, problematic_urls_file):
    """Delete directories associated with URLs listed in the problematic_urls_file, regardless of content."""
    with open(problematic_urls_file, "r") as file:
        urls = file.readlines()

    urls = [url.strip() for url in urls]  # Remove any extra whitespace or newlines
    for url in urls:
        dir_name = sanitize_filename(url)
        dir_path = os.path.join(root_dir, dir_name)
        if os.path.exists(dir_path) and os.path.isdir(dir_path):
            try:
                shutil.rmtree(dir_path)  # Deletes the directory even if it has contents
                print(f"Deleted directory: {dir_path}")
            except OSError as e:
                print(f"Failed to delete {dir_path}. Error: {e}")

def main():
    root_directory = "IMAGE_DIRECTORIES"  # Update this to your directories path
    problematic_urls_file = "error_fixing_urls.txt"  # Update if the file name/location differs
    
    delete_directories(root_directory, problematic_urls_file)

if __name__ == "__main__":
    main()
