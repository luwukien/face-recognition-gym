import os
import pandas as pd

CLEAN_FOLDER= 'cleaned_photos'
clean_ids=[]

for filename in os.listdir(CLEAN_FOLDER):
  if filename.endswith('.png'):
    member_id = filename.split('_@')[0]
    clean_ids.append(member_id)
print(clean_ids)
EXCEL_FILE_PATH = '/home/luwukien/Project/Personal/VisionGym/fake_members.xlsx'
ID_MEMBER = 'Member ID'

df_full = pd.read_excel(EXCEL_FILE_PATH)
df_clean = df_full[df_full[ID_MEMBER].isin(clean_ids)]
print(f"Lọc xong! Đã tìm thấy thông tin của {len(df_clean)} hội viên.")


df_clean.to_csv('members.csv', index=False, encoding='utf-8-sig')


