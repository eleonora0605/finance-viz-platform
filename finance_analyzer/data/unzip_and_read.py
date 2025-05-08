import zipfile
import os

# 壓縮檔案路徑
zip_file = 'finance_analyzer/data/financials_103_to_113.zip'

# 解壓縮後的目標資料夾
extract_folder = 'finance_analyzer/data/financials_103_to_113'

# 解壓縮
with zipfile.ZipFile(zip_file, 'r') as zip_ref:
    zip_ref.extractall(extract_folder)

print(f"檔案已解壓縮到: {extract_folder}")
