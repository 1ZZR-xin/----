import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

# 读取 CSV
df = pd.read_csv("全剧_台词_情感汇总.csv", encoding="utf-8-sig")

# 创建空图
G = nx.Graph()

# 遍历每行，添加节点和边
for _, row in df.iterrows():
    role = row['人物']
    scene = row['剧情阶段']
    emotion = row['情感分类']

    # 添加节点
    G.add_node(role, type='角色')
    G.add_node(scene, type='情节')
    G.add_node(emotion, type='情感')

    # 添加边
    G.add_edge(role, scene, relation='参与')
    G.add_edge(scene, emotion, relation='情感倾向')

# 绘图
plt.figure(figsize=(14, 10))
pos = nx.spring_layout(G, seed=42)  # 节点自动布局

# 节点颜色按类型区分
colors = []
for n in G.nodes(data=True):
    if n[1]['type']=='角色':
        colors.append('skyblue')
    elif n[1]['type']=='情节':
        colors.append('orange')
    else:
        colors.append('lightgreen')

nx.draw(G, pos, with_labels=True, node_color=colors, node_size=2000, font_family='SimHei')
plt.title("《甄嬛传》角色—情节—情感关系图")
plt.show()
