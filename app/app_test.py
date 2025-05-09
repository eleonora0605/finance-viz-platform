import pandas as pd

class FinancialData:
    def __init__(self):
        self.csv_path = "/workspaces/finance-viz-platform/finance_analyzer/data/selected_companies_financials_cleaned.csv"
        self.companies = self._load_data()

    def _load_data(self):
        # 讀取 CSV 檔案
        df = pd.read_csv(self.csv_path)

        companies = {}
        grouped = df.groupby("公司簡稱")  # 確保這裡的名稱與 CSV 檔案一致

        for company, group in grouped:
            company_data = {
                "year": group["年份"].tolist(),
                "code": str(group["公司代號"].iloc[0]),
                "profit_margin": group.set_index("年份")["獲利能力-純益率(%)"].to_dict(),
                "roe": group.set_index("年份")["獲利能力-權益報酬率(%)"].to_dict(),
                "debt_ratio": group.set_index("年份")["財務結構-負債佔資產比率(%)"].to_dict(),
                "eps": group.set_index("年份")["獲利能力-每股盈餘(元)"].to_dict(),
            }
            companies[company] = company_data

        return companies

    def print_companies(self):
        # 列印 self.companies 的內容
        for company, data in self.companies.items():
            print(f"{company}")
            for key, value in data.items():
                print(f"  {key}: {value}")

if __name__ == "__main__":
    financial_data = FinancialData()
    financial_data.print_companies()