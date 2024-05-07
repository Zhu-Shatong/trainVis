import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import requests

import json

def load_data():
    data = pd.read_json('life-expectancy-table.json')
    header = data.iloc[0]  # 第一行是列名
    data = data[1:]  # 剩下的行是数据
    data.columns = header  # 设置列名
    return data

def main():
    st.title('Income since 1950')
    data = load_data()
    

    countries = [
        'Finland', 'France', 'Germany', 'Iceland',
        'Norway', 'Poland', 'Russia', 'United Kingdom'
    ]
    series_list = []
    for country in countries:
        filtered_data = data[(data['Country'] == country) & (data['Year'] >= 1950)]
        series_list.append({
            'type': 'line',
            'name': country,
            'data': filtered_data[['Year', 'Income']].values.tolist(),
            'emphasis': {
                'focus': 'series'
            },
            'showSymbol': False,
            'endLabel': {
                'show': True,
                'formatter': '{@[0]}: {@[1]}'
            },
            'encode': {
                'x': 'Year',
                'y': 'Income',
                'label': ['Country', 'Income'],
                'itemName': 'Year',
                'tooltip': ['Income']
            }
        })
    
    option = {
        'animation': True,
        'animationDuration': 10000,  # 动画持续时间，单位为毫秒
        
        'tooltip': {
            'trigger': 'axis'
        },
        'xAxis': {
            'type': 'category'
        },
        'yAxis': {
            'type': 'value',
            'name': 'Income'
        },
        'series': series_list
    }
    
    st_echarts(options=option, height="600px")

if __name__ == "__main__":
    main()
