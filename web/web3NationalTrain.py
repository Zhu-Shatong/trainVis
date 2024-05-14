import streamlit as st
import streamlit.components.v1 as components


if __name__ == '__main__':

    # 设置页面配置
    st.set_page_config(layout="wide", page_title="全国高铁线路可视化",
                       page_icon=":train:")

    st.title('🚆全国高铁线路可视化')
    tab1, tab2 = st.tabs(["📈 高铁线路全国分布图", "🌐 网络图"])

    with tab1:

        st.title("📈 高铁线路全国分布图")

        boxif = st.selectbox(
            '请选择要显示的航线图',
            ('简化版（流畅）', '完整版'))

        with st.container():
            if boxif == '完整版':
                components.html(
                    open("static/flights_line.html").read(),  width=1485, height=810)
            else:
                components.html(
                    open("static/flights_line_easy.html").read(),  width=1485, height=810)

    with tab2:

        st.title("🌐 网络图")

        components.html(open("static/net.html").read(),
                        width=1485, height=810)
