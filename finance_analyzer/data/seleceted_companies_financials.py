import pandas as pd

folder_path = "/workspaces/finance-viz-platform/finance_analyzer/data/financials_103_to_113/financials_103_to_113"
target_keywords = ['王品', '六角', '漢來', '美食-KY', '美食達人', '瓦城']
merged_df = pd.DataFrame()  # 初始化空的 DataFrame

# 處理103到113年
for year in range(103, 114):
    for market in ["TWSE", "TPEx"]:
        file_name = f"{year}_{market}-utf8.csv"
        file_path = f"{folder_path}/{file_name}" 

        try:
            df = pd.read_csv(file_path)
            df_filtered = df[df['公司簡稱'].str.contains('|'.join(target_keywords), na=False)].copy()
            df_filtered["年份"] = year
            merged_df = pd.concat([merged_df, df_filtered], ignore_index=True)
        except Exception as error:
            print(f"處理檔案 {file_path} 時發生錯誤：{error}")

# 輸出統整後的 CSV 檔案
output_file_path = "/workspaces/finance-viz-platform/finance_analyzer/data/selected_companies_financials.csv"
merged_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')
print("已輸出：", output_file_path)

try:
    df = pd.read_csv(output_file_path)
    columns_to_drop = [
        '財務結構-長期資金佔不動產、廠房及設備比率(%)',
        '經營能力-存貨週轉率(次)',
        '經營能力-平均售貨日數',
        '經營能力-不動產、廠房及設備週轉率(次)',
        '經營能力-總資產週轉率(次)',
        '獲利能力-稅前純益佔實收資本比率(%)',
        '現金流量-現金流量允當比率(%)',
        '現金流量-現金再投資比率(%)'
    ]
    df_cleaned = df.drop(columns=columns_to_drop, errors='ignore')

    # 將「年份」欄位移到最前面
    columns = ['年份'] + [col for col in df_cleaned.columns if col != '年份']
    df_cleaned = df_cleaned[columns]
except Exception as error:
    print(f"清洗檔案失敗，錯誤：{error}")

# 輸出清洗後的 CSV 檔案
cleaned_output_file_path = "/workspaces/finance-viz-platform/finance_analyzer/data/selected_companies_financials_cleaned.csv"
df_cleaned.to_csv(cleaned_output_file_path, index=False, encoding='utf-8-sig')
print("已清洗並輸出：", cleaned_output_file_path)

