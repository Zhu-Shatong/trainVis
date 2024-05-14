import json
import networkx as nx
from pyvis.network import Network


# 解析 JSON 数据
with open('data/RelationChartInfo.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 创建网络图
G = nx.Graph()

# 添加节点和边
for node in data['nodes']:
    G.add_node(node['name'], size=node['value'] * 10,
               title=node['name'], group=node['category'])

for edge in data['edges']:
    G.add_edge(edge['source'], edge['target'])

# 为不同的类别设置不同的颜色
groups = {0: '#FF5733', 1: '#33FFCE', 2: '#9D33FF', 3: '#FFF833'}
for node in G.nodes:
    G.nodes[node]['color'] = groups[G.nodes[node]['group']]

# 使用 Pyvis 创建可交互的网络图
nt = Network('2000px', '2000px', notebook=True)
nt.from_nx(G)


# 调整物理效果参数
nt.barnes_hut(
    gravity=-80000,        # 增加引力
    central_gravity=0.3,
    spring_length=200,     # 调整弹簧长度
    spring_strength=0.05,  # 调整弹簧力度
    damping=0.09           # 增加阻尼
)

nt.show('net.html')
