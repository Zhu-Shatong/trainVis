import streamlit as st
import pandas as pd
from datetime import time


@st.cache_data
def load_data():
    # 读取CSV文件
    df = pd.read_csv('data\sh_price_info_with_distance.csv')
    # 转换 start_time 列为 datetime 类型并去除秒数
    df['start_time'] = pd.to_datetime(
        df['start_time'], format='%H:%M:%S').dt.strftime('%H:%M')
    df['start_time'] = pd.to_datetime(df['start_time'], format='%H:%M').dt.time
    return df


def show_filtered_data(df):
    st.dataframe(df.style.highlight_max(axis=0))
    # Convert the DataFrame to CSV format and create a download button
    csv = df.to_csv().encode('utf-8')
    st.download_button(
        label="下载筛选后的数据",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv',
    )


def filter_data(df, expanded=True):
    # 初始化session state
    if 'departure_station' not in st.session_state:
        st.session_state['departure_station'] = []
    if 'arrival_station' not in st.session_state:
        st.session_state['arrival_station'] = []

    # 添加折叠展开模块
    with st.expander("筛选条件", expanded=expanded):
        # 使用时间滑块选择时间范围
        min_time = time(0, 0)
        max_time = time(23, 59)
        time_range = st.slider("选择时间区间", value=(
            min_time, max_time), format="HH:mm")
        df = df[(df['start_time'] >= time_range[0]) &
                (df['start_time'] <= time_range[1])]

        col1, col2 = st.columns(2)
        with col1:
            # 选择座位等级和价格区间
            seat_classes = ['business_seat', 'first_class_seat', 'second_class_seat',
                            'premium_soft_sleeper', 'soft_sleeper', 'hard_sleeper',
                            'soft_seat', 'hard_seat', 'standing_ticket']
            seat_class = st.selectbox("选择座位等级", options=[''] + seat_classes)
        with col2:
            if seat_class:
                min_price = df[seat_class].min()
                max_price = df[seat_class].max()
                if pd.notna(min_price) and pd.notna(max_price):
                    price_range = st.slider("选择价格区间", min_value=float(min_price), max_value=float(max_price),
                                            value=(float(min_price), float(max_price)))
                    df = df[(df[seat_class] >= price_range[0]) &
                            (df[seat_class] <= price_range[1])]
            else:
                st.warning("请选择座位等级以选择价格区间")

        # 处理出发站和到达站多选框
        col1, col2 = st.columns(2)
        with col1:
            departure_options = df['departure_station'].unique()
            if departure_options.size > 0:
                departure_station = st.multiselect("选择出发站", options=departure_options,
                                                   default=st.session_state['departure_station'])
                st.session_state['departure_station'] = departure_station
                if departure_station:
                    df = df[df['departure_station'].isin(departure_station)]
            else:
                st.warning("没有可用的出发站选项")

        with col2:
            arrival_options = df['arrival_station'].unique()
            if arrival_options.size > 0:
                arrival_station = st.multiselect("选择到达站", options=arrival_options,
                                                 default=st.session_state['arrival_station'])
                st.session_state['arrival_station'] = arrival_station
                if arrival_station:
                    df = df[df['arrival_station'].isin(arrival_station)]
            else:
                st.warning("没有可用的到达站选项")

        # 一键清空筛选规则按钮
        if st.button("清空筛选"):
            keys_to_reset = ['departure_station', 'arrival_station',
                             'time_range', 'seat_class', 'price_range']
            for key in keys_to_reset:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

    if df.empty:
        st.error("当前筛选条件下没有可用的票务信息，请调整筛选条件。")

    return df


if __name__ == '__main__':

    st.title('数据集')

    df = load_data()
    filtered_df = filter_data(df)
    show_filtered_data(filtered_df)
