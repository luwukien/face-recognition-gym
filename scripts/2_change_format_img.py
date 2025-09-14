from pathlib import Path

FOLDER_PATH = Path('data/cleaned_photos') # Sửa lại tên folder của mày ở đây

image_files = list(FOLDER_PATH.glob('*.png')) + list(FOLDER_PATH.glob('*.jpeg'))

for file_path in image_files:
    new_file_path = file_path.with_suffix('.jpg')
    
    file_path.rename(new_file_path)

print("\nTo change img from .png and .jpeg to .jpg")