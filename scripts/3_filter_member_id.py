import os
import pandas as pd

CLEAN_FOLDER= '/home/luwukien/Project/Personal/VisionGym/data/cleaned_photos'
clean_ids=[]

for filename in os.listdir(CLEAN_FOLDER):
  if filename.endswith('.jpg'):
    member_id = filename.split('_@')[0]
    clean_ids.append(member_id)
print(clean_ids)
EXCEL_FILE_PATH = '/home/luwukien/Project/Personal/VisionGym/data/all-report-members.xlsx'
ID_MEMBER = 'Mã hội viên'
  
df_full = pd.read_excel(EXCEL_FILE_PATH)
df_clean = df_full[df_full[ID_MEMBER].isin(clean_ids)]

COLUMNS = ['Mã hội viên', 'Tên Hội viên', 'Ngày đăng ký']
df_selected = df_clean[COLUMNS]


df_selected.to_csv('members.csv', index=False, encoding='utf-8-sig')


