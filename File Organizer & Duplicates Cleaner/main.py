import os
import shutil
import hashlib

# Scans and collects all files from a given directory
class FileScanner:
    def __init__(self, target_dir):
        self.target_dir = target_dir
        self.files = []

    def scan(self):
        # Walk through all directories and subdirectories
        for root, _, filenames in os.walk(self.target_dir):
            for f in filenames:
                full_path = os.path.join(root, f)
                self.files.append(full_path)
        return self.files

# Organizes files into folders based on file extension
class FileOrganizer:
    def __init__(self, files):
        self.files = files

    def organize_by_extension(self):
        for file_path in self.files:
            ext = os.path.splitext(file_path)[1].lower().strip(".")
            if not ext:
                ext = "no_extension"
            folder_path = os.path.join(os.path.dirname(file_path), ext)
            os.makedirs(folder_path, exist_ok=True)
            try:
                shutil.move(file_path, os.path.join(folder_path, os.path.basename(file_path)))
            except Exception as e:
                print(f"[ERROR] Could not move {file_path}: {e}")

# Finds and removes duplicate files based on file content (hash)
class DuplicateFinder:
    def __init__(self, files):
        self.files = files

    def file_hash(self, file_path):
        hash_algo = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                while chunk := f.read(8192):
                    hash_algo.update(chunk)
            return hash_algo.hexdigest()
        except:
            return None

    def find_duplicates(self):
        seen = {}
        duplicates = []
        for file in self.files:
            filehash = self.file_hash(file)
            if not filehash:
                continue
            if filehash in seen:
                duplicates.append(file)
            else:
                seen[filehash] = file
        return duplicates

    def remove_duplicates(self, duplicates):
        for dup in duplicates:
            try:
                os.remove(dup)
                print(f"[REMOVED] Duplicate file: {dup}")
            except Exception as e:
                print(f"[ERROR] Could not remove {dup}: {e}")

if __name__ == "__main__":
    # Get the folder path from user input
    folder = input("Enter the path of the folder to organize: ").strip()

    print("\n[1] Scanning Files...")
    scanner = FileScanner(folder)
    files = scanner.scan()

    print("[2] Organizing Files by Extension...")
    organizer = FileOrganizer(files)
    organizer.organize_by_extension()

    print("[3] Finding Duplicates...")
    scanner = FileScanner(folder)  # Re-scan after moving files
    files = scanner.scan()
    dup_finder = DuplicateFinder(files)
    duplicates = dup_finder.find_duplicates()

    if duplicates:
        print(f"Found {len(duplicates)} duplicate(s). Removing...")
        dup_finder.remove_duplicates(duplicates)
    else:
        print("No duplicates found.")

    print("\n[✔] Done!")
