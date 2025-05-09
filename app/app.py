# -*- coding: utf-8 -*-z
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import plotly.graph_objects as go
import plotly.express as px

# 設置頁面配置
st.set_page_config(
    page_title="餐飲業財務分析儀表板",
    page_icon="🍽️",
    layout="wide"
)

# 添加自定義CSS
st.markdown("""
<style>
    .main {
        background-color: #FFF5F0;
    }
    .stApp {
        max-width: 1200px;
        margin: 0 auto;
    }
    h1, h2, h3 {
        color: #581845;
    }
    .stButton>button {
        background-color: #FF5733;
        color: white;
    }
    .stButton>button:hover {
        background-color: #C70039;
    }
    .highlight {
        background-color: #FFF5F0;
        padding: 20px;
        border-radius: 10px;
        border-left: 5px solid #FF5733;
    }
    .risk {
        background-color: #FFE5E5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #C70039;
        margin-bottom: 10px;
    }
    .opportunity {
        background-color: #E5FFE5;
        padding: 15px;
        border-radius: 10px;
        border-left: 5px solid #4CAF50;
        margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# 財務數據類
class FinancialData:
    def __init__(self):
        self.csv_path = "/workspaces/finance-viz-platform/app/selected_companies_financials_cleaned.csv"
        self.companies = self._load_data()
        self.risk_highlight = self._risk_highlight_data()
        self.metric_names = self._metric_names()  # 確保這裡正確呼叫 _metric_names
        self.years = self._years()

    def _load_data(self):
        # 讀取 CSV 檔案
        df = pd.read_csv(self.csv_path)
        companies = {}
        grouped = df.groupby("公司簡稱")  # 確保這裡的名稱與 CSV 檔案一致

        for company, group in grouped:
            company_data = {
                "code": str(group["公司代號"].iloc[0]),
                "revenue_growth": group.set_index("年份")["成長能力-營收成長率(%)"].to_dict(),
                "profit_margin": group.set_index("年份")["獲利能力-純益率(%)"].to_dict(),
                "roe": group.set_index("年份")["獲利能力-權益報酬率(%)"].to_dict(),
                "debt_ratio": group.set_index("年份")["財務結構-負債佔資產比率(%)"].to_dict(),
                "eps": group.set_index("年份")["獲利能力-每股盈餘(元)"].to_dict(),
            }
            companies[company] = company_data

        return companies
        
    def _risk_highlight_data(self):
        #初始化風險與亮點分析數據
        return {
            "美食-KY": {
                "111": {
                    "risks": [
                        "原物料成本上升壓縮利潤",
                        "國際連鎖咖啡品牌競爭加劇",
                        "疫情後消費習慣改變"
                    ],
                    "highlights": [
                        "數位轉型成效顯著，線上訂購成長",
                        "新產品線受到市場歡迎",
                        "營收成長率回升至8.5%"
                    ]
                },
                "112": {
                    "risks": [
                        "人力成本持續上升",
                        "租金成本增加",
                        "通膨壓力影響消費意願"
                    ],
                    "highlights": [
                        "會員經濟效益顯現",
                        "海外市場穩定成長",
                        "ESG策略獲得正面評價"
                    ]
                },
                "113": {
                    "risks": [
                        "市場競爭持續激烈",
                        "食品安全法規趨嚴",
                        "原物料價格波動"
                    ],
                    "highlights": [
                        "新店型展店策略成功",
                        "產品創新帶動客單價提升",
                        "數位行銷效益顯著"
                    ]
                }
            },
            "瓦城": {
                "111": {
                    "risks": [
                        "餐飲業人才短缺問題",
                        "多品牌管理複雜度增加",
                        "食材成本上漲"
                    ],
                    "highlights": [
                        "多品牌策略成功，市場覆蓋率高",
                        "營收成長率達15.8%",
                        "數位點餐系統提升營運效率"
                    ]
                },
                "112": {
                    "risks": [
                        "新品牌發展不確定性",
                        "國際擴張風險",
                        "消費者口味快速變化"
                    ],
                    "highlights": [
                        "高毛利新品牌表現亮眼",
                        "會員數持續成長",
                        "供應鏈優化降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "品牌老化風險",
                        "同業複製模式競爭",
                        "租金成本持續上升"
                    ],
                    "highlights": [
                        "品牌年輕化策略成功",
                        "海外市場貢獻增加",
                        "數位轉型成效顯著"
                    ]
                }
            },
            "王品": {
                "111": {
                    "risks": [
                        "高端餐飲市場競爭加劇",
                        "食材成本波動大",
                        "多品牌管理挑戰"
                    ],
                    "highlights": [
                        "疫後消費復甦明顯",
                        "新品牌發展順利",
                        "數位會員經濟成效顯著"
                    ]
                },
                "112": {
                    "risks": [
                        "中高價位餐飲受經濟環境影響大",
                        "人才流失風險",
                        "租金成本持續上升"
                    ],
                    "highlights": [
                        "品牌重塑策略成功",
                        "營運效率持續提升",
                        "多元化收入來源"
                    ]
                },
                "113": {
                    "risks": [
                        "消費者偏好快速變化",
                        "國際擴張不確定性",
                        "食品安全風險"
                    ],
                    "highlights": [
                        "高端市場領導地位鞏固",
                        "數位轉型成效顯著",
                        "ESG策略獲得正面評價"
                    ]
                }
            },
            "漢來美食": {
                "111": {
                    "risks": [
                        "快速擴張帶來的管理風險",
                        "品質一致性挑戰",
                        "中低價位市場競爭激烈"
                    ],
                    "highlights": [
                        "多元化餐飲品牌組合",
                        "數位點餐系統普及",
                        "外送業務成長顯著"
                    ]
                },
                "112": {
                    "risks": [
                        "原物料成本上升",
                        "人力成本增加",
                        "市場競爭加劇"
                    ],
                    "highlights": [
                        "新店型展店策略成功",
                        "會員經濟效益顯現",
                        "供應鏈整合降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "市場飽和風險",
                        "消費者偏好變化快速",
                        "食品安全法規趨嚴"
                    ],
                    "highlights": [
                        "產品創新帶動成長",
                        "數位行銷效益顯著",
                        "海外市場拓展順利"
                    ]
                }
            },
            "六角": {
                "111": {
                    "risks": [
                        "咖啡市場競爭激烈",
                        "原物料成本上升",
                        "租金成本增加"
                    ],
                    "highlights": [
                        "多品牌策略成功",
                        "數位轉型成效顯著",
                        "會員經濟效益顯現"
                    ]
                },
                "112": {
                    "risks": [
                        "國際擴張風險",
                        "品牌間同質化風險",
                        "人才短缺問題"
                    ],
                    "highlights": [
                        "ESG策略獲得正面評價",
                        "產品創新帶動客單價提升",
                        "供應鏈優化降低成本"
                    ]
                },
                "113": {
                    "risks": [
                        "市場飽和風險",
                        "消費者偏好變化快速",
                        "食品安全法規趨嚴"
                    ],
                    "highlights": [
                        "海外市場貢獻增加",
                        "數位會員經濟成效顯著",
                        "新店型展店策略成功"
                    ]
                }
            }
        }
    def _metric_names(self):
        #初始化指標名稱
        return{
            "revenue_growth": "營收成長率 (%)",
            "profit_margin": "淨利率 (%)",
            "roe": "股東權益報酬率 (%)",
            "debt_ratio": "負債比率 (%)",
            "eps": "每股盈餘 (元)"
        }
        
    def _years(self):
        # 年度列表
        self.years = ["103", "104", "105", "106", "107", "108", "109", "110", "111", "112", "113"]
        return self.years
    
    def get_company_names(self):
        """獲取所有公司名稱"""
        return list(self.companies.keys())
    
    def get_company_code(self, company_name):
        """獲取公司代碼"""
        return self.companies[company_name]["code"]
    
    def get_metric_names(self):
        """獲取所有指標名稱"""
        return self.metric_names
    
    def get_years(self):
        """獲取所有年度"""
        return self.years
    
    def get_data_for_years(self, company_name, metric, years_range):
        """獲取特定年份範圍的數據"""
        if years_range == 5:
            selected_years = self.years[-5:]
        else:  # 10年
            selected_years = self.years[-10:]
        
        return {year: self.companies[company_name][metric].get(str(year), 0) for year in selected_years}
    
    def get_risk_highlight(self, company_name, year):
        """獲取風險與亮點分析"""
        if company_name in self.risk_highlight and year in self.risk_highlight[company_name]:
            return self.risk_highlight[company_name][year]
        else:
            return {"risks": ["無該年度風險資料"], "highlights": ["無該年度亮點資料"]}


# 圖表生成類
class ChartGenerator:
    def __init__(self, financial_data):
        self.financial_data = financial_data
    
    def generate_line_chart(self, selected_companies, metric, years_range):
        """生成折線圖"""
        if years_range == 5:
            selected_years = self.financial_data.get_years()[-5:]
        else:  # 10年
            selected_years = self.financial_data.get_years()[-10:]
        
        fig = go.Figure()
        
        for company in selected_companies:
            data = self.financial_data.get_data_for_years(company, metric, years_range)
            values = [data.get(year, None) for year in selected_years]
            
            fig.add_trace(go.Scatter(
                x=selected_years,
                y=values,
                mode='lines+markers',
                name=f"{company} ({self.financial_data.get_company_code(company)})",
                line=dict(width=3),
                marker=dict(size=8)
            ))
        
        fig.update_layout(
            title=f"{self.financial_data.get_metric_names()[metric]} 趨勢圖",
            xaxis_title="年度",
            yaxis_title=self.financial_data.get_metric_names()[metric],
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            template="seaborn",
            height=500,
        )
        
        # 添加年度標籤
        fig.update_xaxes(
            ticktext=[f"{year}年" for year in selected_years],
            tickvals=selected_years
        )
        
        return fig
    
    def generate_comparison_table(self, company, year):
        """生成年度比較表格數據"""
        prev_year = str(int(year) - 1)
        metrics = ["revenue_growth", "profit_margin", "roe", "debt_ratio", "eps"]
        
        comparison_data = []
        
        for metric in metrics:
            current_value = self.financial_data.companies[company][metric].get(year,0)
            prev_value = self.financial_data.companies[company][metric].get(prev_year,0)
            change = current_value - prev_value
            change_percent = (change / prev_value * 100) if prev_value != 0 else 0
            
            # 負債比率下降為正面
            if metric == "debt_ratio":
                change_direction = "↓" if change < 0 else "↑"
                change_class = "positive" if change < 0 else "negative"
            else:
                change_direction = "↑" if change > 0 else "↓"
                change_class = "positive" if change > 0 else "negative"
            
            comparison_data.append({
                "metric": self.financial_data.metric_names[metric],
                "prev_value": round(prev_value, 2),
                "current_value": round(current_value, 2),
                "change": round(abs(change), 2),
                "change_percent": round(abs(change_percent), 2),
                "change_direction": change_direction,
                "change_class": change_class
            })
        
        return comparison_data, prev_year


# 應用程序類
class FinancialAnalysisApp:
    def __init__(self):
        self.financial_data = FinancialData()
        self.chart_generator = ChartGenerator(self.financial_data)
    
    def run(self):
        """運行應用程序"""
        st.markdown("<h1 style='text-align: center; color: #581845;'>餐飲業財務分析儀表板</h1>", unsafe_allow_html=True)
        
        # 側邊欄 - 公司選擇
        st.sidebar.markdown("### 選擇分析參數")
        
        # 公司多選
        company_names = self.financial_data.get_company_names()
        if not company_names:
            st.error("無可用的公司資料")
            return
        selected_companies = st.sidebar.multiselect(
            "選擇感興趣的公司",
            company_names,
            default=[company_names[0]] if company_names else []
        )

        # 時間範圍選擇
        years_range = st.sidebar.radio(
            "選擇時間範圍",
            [5, 10],
            format_func=lambda x: f"近{x}年"
        )
        
        # 財務指標選擇
        selected_metric = st.sidebar.selectbox(
            "選擇財務指標",
            list(self.financial_data.get_metric_names().keys()),
            format_func=lambda x: self.financial_data.get_metric_names()[x]
        )
        
        # 主要內容區域
        if not selected_companies:
            st.warning("請至少選擇一家公司進行分析")
            return
        
        # 生成圖表
        st.markdown("### 財務指標趨勢圖")
        fig = self.chart_generator.generate_line_chart(selected_companies, selected_metric, years_range)
        st.plotly_chart(fig, use_container_width=True)
        
        # 分隔線
        st.markdown("---")
        
        # 詳細分析區域
        st.markdown("### 詳細財務分析")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            # 公司選擇
            company_for_detail = st.selectbox(
                "選擇公司",
                selected_companies,
                key="company_detail"
            )
        
        with col2:
            # 年度選擇
            available_years = self.financial_data.get_years()[-5:] if years_range == 5 else self.financial_data.get_years()[-10:]
            if not available_years:
                st.warning("無可用的年度資料")
                return
            selected_year = st.selectbox(
                "選擇年度",
                available_years,
                index=len(available_years)-1 if available_years else 0,
                format_func=lambda x: f"{x}年",
                key="year_detail"
            )
        
        # 生成比較表格
        comparison_data, prev_year = self.chart_generator.generate_comparison_table(company_for_detail, selected_year)
        
        st.markdown(f"#### {company_for_detail} ({self.financial_data.get_company_code(company_for_detail)}) {selected_year}年 vs {prev_year}年 財務比較")
        
        # 使用DataFrame顯示比較表格
        df = pd.DataFrame(comparison_data)
        
        # 格式化顯示
        formatted_df = pd.DataFrame({
            "財務指標": df["metric"],
            f"{prev_year}年": df["prev_value"],
            f"{selected_year}年": df["current_value"],
            "變化": [f"{row['change_direction']} {row['change']} ({row['change_percent']}%)" for _, row in df.iterrows()]
        })
        
        # 顯示表格
        st.dataframe(
            formatted_df,
            use_container_width=True,
            hide_index=True
        )
        
        # 風險與亮點分析
        st.markdown("#### 投資風險與亮點分析")
        
        risk_highlight = self.financial_data.get_risk_highlight(company_for_detail, selected_year)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="risk">', unsafe_allow_html=True)
            st.markdown("##### 潛在風險")
            for risk in risk_highlight["risks"]:
                st.markdown(f"- {risk}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="opportunity">', unsafe_allow_html=True)
            st.markdown("##### 投資亮點")
            for highlight in risk_highlight["highlights"]:
                st.markdown(f"- {highlight}")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # 公司基本資訊卡片
        st.markdown("#### 公司基本資訊")
        
        company_info = {
            "美食-KY": {
                "full_name": "美食-KY",
                "industry": "連鎖咖啡烘焙",
                "founded": "2004年",
                "stores": "全球超過1,000家門市",
                "description": "以現烤麵包、現煮咖啡聞名的連鎖咖啡烘焙店，在台灣、中國、美國等地均有據點。"
            },
            "瓦城": {
                "full_name": "瓦城泰統集團",
                "industry": "連鎖餐飲",
                "founded": "1990年",
                "stores": "超過100家門市",
                "description": "以泰式料理起家，旗下擁有瓦城、非常泰、1010湘、十食湘、時時香、YABI等多個品牌。"
            },
            "王品": {
                "full_name": "王品集團",
                "industry": "連鎖餐飲",
                "founded": "1993年",
                "stores": "超過400家門市",
                "description": "台灣知名連鎖餐飲集團，旗下擁有王品牛排、陶板屋、西堤、夏慕尼等多個品牌。"
            },
            "漢來美食": {
                "full_name": "漢來美食股份有限公司",
                "industry": "連鎖餐飲",
                "founded": "1996年",
                "stores": "超過200家門市",
                "description": "以平價美食聞名，旗下擁有多個中式、日式、西式餐飲品牌，主打年輕消費族群。"
            },
            "六角": {
                "full_name": "六角國際事業股份有限公司",
                "industry": "連鎖咖啡餐飲",
                "founded": "1998年",
                "stores": "超過300家門市",
                "description": "以咖啡起家，旗下擁有cama café、路易莎咖啡、棉花田等多個品牌，近年積極拓展海外市場。"
            }
        }
        
        info = company_info[company_for_detail]
        
        st.markdown(f"""
        <div class="highlight">
            <h5>{company_for_detail} ({self.financial_data.get_company_code(company_for_detail)}) - {info['full_name']}</h5>
            <p><strong>產業類別:</strong> {info['industry']}</p>
            <p><strong>成立時間:</strong> {info['founded']}</p>
            <p><strong>門市規模:</strong> {info['stores']}</p>
            <p><strong>公司簡介:</strong> {info['description']}</p>
        </div>
        """, unsafe_allow_html=True)


# 執行應用程序
if __name__ == "__main__":
    app = FinancialAnalysisApp()
    app.run()