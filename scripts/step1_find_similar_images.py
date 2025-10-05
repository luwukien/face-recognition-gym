import os
import shutil
from PIL import Image
import imagehash

SOURCE_FOLDER = '/home/luwukien/Project/Personal/MemberPhoto'

CLEAN_FOLDER = '/home/luwukien/Project/Personal/VisionGym/data/cleaned_photos'
TRASH_FOLDER = '/home/luwukien/Project/Personal/VisionGym/data/redudant_photos'
os.makedirs(CLEAN_FOLDER, exist_ok=True)
os.makedirs(TRASH_FOLDER, exist_ok=True)

hashes={}
for filename in os.listdir(SOURCE_FOLDER):
    if filename.endswith(('.png', 'jpg', '.jpeg')):
        image_path = os.path.join(SOURCE_FOLDER, filename)
    try:
        hash_values = str(imagehash.phash(Image.open(image_path)))
        if hash_values in hashes:
            hashes[hash_values].append(image_path)
        else:
            hashes[hash_values] = [image_path]
    except Exception as e:
        print("Error: ", e)

#Filter similar img
for hash_value, file_list in hashes.items(): 
    representative_file = file_list[0]
    shutil.copy(representative_file, os.path.join(CLEAN_FOLDER, os.path.basename(representative_file)))

    if len(file_list) > 1:
        redudant_files = file_list[1:]
        for file_path in redudant_files:
            shutil.move(file_path, os.path.join(TRASH_FOLDER, os.path.basename(file_path)))
            print("Moved file to trash folder")
    
