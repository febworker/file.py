import os
import shutil
import unicodedata
def normalize(filename):
    normalized_name = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore').decode('utf-8')
    normalized_name = ''.join(['_' if not c.isalnum() else c for c in normalized_name])
    return normalized_name
def sort_folder(folder_path):
    categories = {
        'images': ['jpeg', 'jpg', 'png', 'svg'],
        'videos': ['avi', 'mp4', 'mov', 'mkv'],
        'documents': ['doc', 'docx', 'txt', 'pdf', 'xlsx', 'pptx'],
        'audio': ['mp3', 'ogg', 'wav', 'amr'],
        'archives': ['zip', 'gz', 'tar']
    }
    unknown_extensions = set()
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            file_name, file_extension = os.path.splitext(file)
            file_extension = file_extension.lower()[1:]
            new_name = normalize(file_name) + file_extension
            category = None
            for cat, exts in categories.items():
                if file_extension in exts:
                    category = cat
                    break
            if category:
                category_folder = os.path.join(folder_path, category)
                if not os.path.exists(category_folder):
                    os.makedirs(category_folder)
                shutil.move(os.path.join(root, file), os.path.join(category_folder, new_name))
            else:
                unknown_extensions.add(file_extension)
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for dir in dirs:
            dir_path = os.path.join(root, dir)
            if not os.listdir(dir_path):
                os.rmdir(dir_path)
    return list(categories.keys()), list(unknown_extensions)
if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: python sort.py <folder_path>")
        sys.exit(1)
    folder_path = sys.argv[1]
    categories, unknown_extensions = sort_folder(folder_path)
    print("Files sorted into categories:")
    for category in categories:
        print(f"{category}:")
        category_path = os.path.join(folder_path, category)
        for file in os.listdir(category_path):
            print(f"  - {file}")
    print("\nUnknown extensions:")
    for ext in unknown_extensions:
        print(ext)