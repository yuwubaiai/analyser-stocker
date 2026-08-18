python

import streamlit as st

import pandas as pd

import numpy as np

st.set_page_config(page_title="股票分析框架", layout="wide", initial_sidebar_state="collapsed")

st.title("📊 股票分析框架（业绩+估值+分红+可信度）")

st.caption("跨端通用版 · 手机电脑均可访问")

内置演示数据

data = {

"代码": ["600519", "000333", "600036", "300750", "601318", "000858", "002594", "600900"],

"名称": ["贵州茅台", "美的集团", "招商银行", "宁德时代", "中国平安", "五粮液", "比亚迪", "长江电力"],

"ROE": [32, 24, 16, 18, 12, 25, 8, 15],

"净利CAGR": [18, 12, 10, 45, 8, 14, 35, 6],

"净现比": [1.05, 1.2, 0.9, 0.8, 1.1, 1.0, 0.7, 1.3],

"PE": [22, 14, 8, 35, 10, 20, 25, 18],

"PE分位": [28, 15, 5, 80, 30, 40, 60, 10],

"PEG": [0.9, 0.8, 0.5, 1.5, 0.7, 1.1, 1.2, 1.0],

"股息率": [2.1, 3.5, 4.2, 0.5, 3.8, 2.5, 0.8, 4.5],

"分红年数": [11, 10, 12, 4, 9, 8, 5, 15],

"负债率": [18, 65, 92, 55, 90, 20, 70, 40],

"审计": ["标准无保留", "标准无保留", "标准无保留", "标准无保留", "标准无保留", "标准无保留", "标准无保留", "标准无保留"],

"质押率": [0, 5, 0, 10, 2, 0, 15, 0],

"频繁换所": [False, False, False, False, False, False, True, False],

"高管减持": [False, False, False, True, False, False, True, False]

}

df = pd.DataFrame(data)

侧边栏筛选

st.sidebar.header("筛选条件")

roe_min = st.sidebar.slider("ROE ≥", 0, 30, 10)

g_min = st.sidebar.slider("净利CAGR ≥", -20, 60, 10)

pe_max = st.sidebar.slider("PE ≤", 0, 80, 30)

div_min = st.sidebar.slider("股息率 ≥", 0.0, 8.0, 2.5, 0.1)

debt_max = st.sidebar.slider("负债率 ≤", 0, 100, 60)

过滤逻辑

filtered_df = df[

(df["ROE"] >= roe_min) &

(df["净利CAGR"] >= g_min) &

(df["PE"] <= pe_max) &

(df["股息率"] >= div_min) &

(df["负债率"] <= debt_max)

]

红绿灯判断

def get_tag(row):

if row["ROE"] >= 15 and row["PE"] <= 20 and row["股息率"] >= 3:

return "🟢 优质"

elif row["ROE"] >= 10 and row["PE"] <= 30:

return "🟡 观察"

else:

return "🔴 谨慎"

filtered_df["标签"] = filtered_df.apply(get_tag, axis=1)

显示结果

st.subheader(f"命中列表 ({len(filtered_df)} 只)")

st.dataframe(filtered_df[["代码", "名称", "ROE", "PE", "股息率", "标签"]], use_container_width=True)

四栏明细

st.subheader("四栏明细")

for _, row in filtered_df.iterrows():

with st.container():

st.markdown(f"### {row['名称']} ({row['代码']}) —— {row['标签']}")

c1, c2, c3, c4 = st.columns(4)

c1.metric("业绩", f"ROE {row['ROE']}%", f"CAGR {row['净利CAGR']}%")

c2.metric("估值", f"PE {row['PE']}", f"分位 {row['PE分位']}%")

c3.metric("分红", f"{row['股息率']}%", f"连分{row['分红年数']}年")

c4.metric("可信度", row['审计'], f"质押{row['质押率']}%")

st.divider()
