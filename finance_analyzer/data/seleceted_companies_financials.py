import pandas as pd
import os

# 定義資料夾路徑
folder_path = "/workspaces/finance-viz-platform/finance_analyzer/data/financials_103_to_113/financials_103_to_113"

# 定義目標公司關鍵字
target_keywords = ['王品', '六角', '漢來', '美食-KY', '美食達人', '瓦城']

# 初始化儲存合併資料的 DataFrame
merged_df = pd.DataFrame()

# 逐年處理103到113年
for year in range(103, 114):
    for market in ["TWSE", "TPEx"]:
        file_name = f"{year}_{market}-utf8.csv"
        file_path = os.path.join(folder_path, file_name)
        
        if os.path.exists(file_path):
            try:
                df = pd.read_csv(file_path)
                df_filtered = df[df['公司簡稱'].str.contains('|'.join(target_keywords), na=False)].copy()
                df_filtered["年份"] = year
                merged_df = pd.concat([merged_df, df_filtered], ignore_index=True)
            except Exception as e:
                print(f"讀取檔案失敗：{file_path}，錯誤：{e}")
        else:
            print(f"找不到檔案：{file_path}")

# 輸出統整後的 CSV 檔案
output_file_path = "/workspaces/finance-viz-platform/finance_analyzer/data/selected_companies_financials.csv"
merged_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
print("✅ 已輸出：", output_file_path)
