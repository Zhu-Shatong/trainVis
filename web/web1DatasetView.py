import streamlit as st
import pandas as pd
from datetime import time
import streamlit.components.v1 as components

from plotDataset import Dataset_TreeMap

if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="数据集与任务一览",
                       page_icon=":mag:")

    st.title('🚈高铁数据可视化🚈')

    st.write("""
            2151131 朱沙桐 数据科学与大数据技术
            """)

    st.title('🚃数据集与任务一览')

    st.subheader("树图")

    st.plotly_chart(Dataset_TreeMap(), use_container_width=True, theme=None)
