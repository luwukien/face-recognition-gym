from pathlib import Path
from PIL import Image

FOLDER_PATH = Path('/home/luwukien/Project/Personal/VisionGym/data/cleaned_photos')

# The numbers extendsion of file
EXTENSIONS_TO_CONVERT = ['.png', '.jpeg', '.webp', '.tiff', '.jpg.png']

print("Starting file format conversion ----")

image_files = []
for ext in EXTENSIONS_TO_CONVERT:
    image_files.extend(list(FOLDER_PATH.rglob(f'*{ext}')))

if not image_files:
    print("Not found any image to convert")
else:
    for file_path in image_files:
        name = file_path.stem #Getting name file without extention file
        if name.endswith(".jpg"): 
            name = name[:-4]

        new_file_path = file_path.with_name(name + ".jpg")

        try:
            with Image.open(file_path) as img:
                rgb_img = img.convert("RGB")  
                #Convert to RGB because PNG can include 4 channel or 3 channel: RGBA / RGB
                rgb_img.save(new_file_path, "JPEG", quality=95)
            file_path.unlink()  
            print(f"Converted {file_path.name} -> {new_file_path.name}")
        except Exception as e:
            print(f"ERROR file {file_path.name}: {e}")

    print("\nFinished!")
