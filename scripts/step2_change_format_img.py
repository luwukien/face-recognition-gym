from pathlib import Path
import os

FOLDER_PATH = Path('data/raw_photos') 

EXTENSIONS_TO_CONVERT = ['.png', '.jpeg', '.webp', '.tiff']

print("Starting file change format image----")

image_files = []
for ext in EXTENSIONS_TO_CONVERT:
    image_files.extend(list(FOLDER_PATH.rglob(f'*{ext}')))

if not image_files:
    print("Not found the imgage to need convert")
else:
    
    for file_path in image_files:
        new_file_path = file_path.with_suffix('.jpg')
        
        try:
            file_path.rename(new_file_path)
        except Exception as e:
            print(f"ERROR file {file_path.name}: {e}")

    print("\nFinished!")