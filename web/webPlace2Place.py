import matplotlib.pyplot as plt
import streamlit as st

from plotPlace2Place import p2pMain,AxsScatter

plt.rcParams['font.sans-serif'] = ['SimHei']  # SimHei 指定中文字体为黑体
plt.rcParams['axes.unicode_minus'] = False  # 显示负号

if __name__ == '__main__':
    st.title('控球区域和排名分析')
    tab1, tab2 = st.tabs(["📈 德甲球队控球位置占比", "🗃 积分和控球区域的关系"])
    with tab1:
        fig = p2pMain()
        st.pyplot(fig)
    with tab2:
        fig=AxsScatter()
        st.plotly_chart(fig, theme="streamlit", use_container_width=True)

