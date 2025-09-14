from pathlib import Path

FOLDER_PATH = Path('cleaned_photos') # Sửa lại tên folder của mày ở đây

image_files = list(FOLDER_PATH.glob('*.png')) + list(FOLDER_PATH.glob('*.jpeg'))

for file_path in image_files:
    # .with_suffix('.jpg') là hàm thần thánh để thay đổi đuôi file
    new_file_path = file_path.with_suffix('.jpg')
    
    print(f'Đang đổi: "{file_path.name}"  ==>  "{new_file_path.name}"')
    file_path.rename(new_file_path)

print("\nĐã lột xác cho cả đống ảnh xong, mời sếp duyệt!")