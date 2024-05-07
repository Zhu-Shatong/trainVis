import streamlit as st
from streamlit_echarts import st_echarts
import pandas as pd
import json

# 加载数据
def load_data():
    station_info = pd.read_json('static/data/StationInfo.json')
    train_info = pd.read_json('static/data/MergedTrainInfo.json')
    station_geo = pd.read_json('static/data/StationGeo.json')
    map_style = json.load(open('static/data/MapStyleConfig.json'))
    return station_info, train_info, station_geo, map_style

station_info, train_info, station_geo, map_style = load_data()

def main():
    st.title("火车站点和线路可视化")

    # Baidu Map API Key
    baidu_api_key = "oW6rKW22HTQjgpFGsRqhfspazDpwYaPy"

    bmap_options = {
        "bmap": {
            "center": [104.114129, 37.550339],
            "zoom": 6,
            "roam": True,
            "mapStyle": {
                'styleJson': [
                    # 这里可以定义百度地图的样式配置
                ]
            }
        },
        "series": [
            {
                "type": 'scatter',
                "coordinateSystem": 'bmap',
                "data": [
                    # 这里放置散点数据
                ]
            },
            {
                "type": 'lines',
                "coordinateSystem": 'bmap',
                "data": [
                    
                    # 这里放置线路数据
                ]
            }
        ]
    }

    # 渲染百度地图
    bmap_html = f"""
    <div id="main" style="width:100%;height:600px;"></div>
    <script type="text/javascript">
        function init() {{
            // 初始化地图
            var map = new BMap.Map("main");
            var point = new BMap.Point(116.404, 39.915);
            map.centerAndZoom(point, 15);
            map.enableScrollWheelZoom(true);

            // 加载ECharts
            var chart = echarts.init(document.getElementById('main'));
            chart.setOption({{option}});
        }}
        init();
    </script>
    <script type="text/javascript" src="https://api.map.baidu.com/api?v=3.0&ak={baidu_api_key}"></script>
    <script src="https://cdn.jsdelivr.net/npm/echarts/dist/echarts.min.js"></script>
    """
    st.components.v1.html(bmap_html, height=600)

    # 使用st_echarts渲染ECharts图表
    st_echarts(options=bmap_options, height="600px")

if __name__ == "__main__":
    main()
