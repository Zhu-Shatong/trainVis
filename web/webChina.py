import matplotlib.pyplot as plt
import streamlit as st
from plotChina import rankPlot,winRatePlot,statsPlot

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号


if __name__ == '__main__':
    st.title('亚洲杯小组赛对手分析')
    tab1,tab2,tab3 = st.tabs(["📈 积分和身价对比","🐾 胜率展示","🤣 数据对比"])
    with tab1:
        fig1 = rankPlot()
        st.plotly_chart(fig1, theme="streamlit", use_container_width=True)
    with tab2:
        fig2 = winRatePlot()
        st.plotly_chart(fig2, theme="streamlit", use_container_width=True)
    with tab3:
        fig3 = statsPlot()
        st.plotly_chart(fig3, theme="streamlit", use_container_width=True)