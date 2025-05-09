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

cleaned_output_file_path = "/workspaces/finance-viz-platform/finance_analyzer/data/selected_companies_financials_cleaned.csv"
# 清洗資料
try:
    # 讀取輸出的 CSV 檔案
    df = pd.read_csv(output_file_path)

    # 刪除不需要的欄位
    columns_to_drop = [ '財務結構-長期資金佔不動產、廠房及設備比率(%)',
                   '經營能力-存貨週轉率(次)',
                   '經營能力-平均售貨日數',
                   '經營能力-不動產、廠房及設備週轉率(次)',
                   '經營能力-總資產週轉率(次)',
                   '獲利能力-稅前純益佔實收資本比率(%)',
                   '現金流量-現金流量允當比率(%)',
                   '現金流量-現金再投資比率(%)']
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

    # 將「年份」欄位移到最前面
    columns = ['年份'] + [col for col in df_cleaned.columns if col != '年份']
    df_cleaned = df_cleaned[columns]

    # 將清洗後的資料另存為新的 CSV 檔案
    df_cleaned.to_csv(cleaned_output_file_path, index=False, encoding='utf-8-sig')
    print("✅ 已清洗並輸出：", cleaned_output_file_path)
except Exception as e:
    print(f"清洗檔案失敗，錯誤：{e}")
