import pandas as pd
import plotly.graph_objects as go

# 读取 CSV
df = pd.read_csv("全剧_台词_情感汇总.csv", encoding="utf-8-sig")

# 指定主要角色
main_roles = ['甄嬛', '华妃', '安陵容', '沈眉庄', '皇上']
df_main = df[df['人物'].isin(main_roles)]

# 获取全部剧情阶段，保证完整显示
all_scenes = df['剧情阶段'].unique().tolist()
# 按数字顺序排序（如果剧情阶段可解析为数字）
# all_scenes.sort(key=lambda x: int(''.join(filter(str.isdigit, x))))
scenes_ordered = all_scenes

# 统计角色→剧情台词数量
role_scene = df_main.groupby(['人物', '剧情阶段']).size().reset_index(name='count')

# 统计剧情→情感台词数量（只保留 top5 情感，避免图太乱）
scene_emotion = df_main.groupby(['剧情阶段', '情感分类']).size().reset_index(name='count')
top_emotions = scene_emotion.groupby('情感分类')['count'].sum().sort_values(ascending=False).head(5).index.tolist()
scene_emotion = scene_emotion[scene_emotion['情感分类'].isin(top_emotions)]

# 创建节点列表（角色 + 全部剧情阶段 + 情感）
roles = role_scene['人物'].unique().tolist()
scenes = scenes_ordered
emotions = list(scene_emotion['情感分类'].unique())
nodes = roles + scenes + emotions

node_indices = {name: i for i, name in enumerate(nodes)}

# 颜色设置
role_colors = ["#1f77b4", "#2ca02c", "#ff7f0e", "#d62728", "#9467bd"]
emotion_colors_map = {
    "喜悦": "lightgreen",
    "愤怒": "red",
    "悲伤": "blue",
    "恐惧": "purple",
    "惊讶": "yellow",
    "厌恶": "gray",
    "中性": "lightgray"
}

# 创建边
source = []
target = []
value = []
link_color = []
label_info = []

# 角色→剧情
for role in roles:
    for scene in scenes:
        # 获取台词数量，如果没有则为0
        count = role_scene[(role_scene['人物']==role) & (role_scene['剧情阶段']==scene)]['count'].sum()
        source.append(node_indices[role])
        target.append(node_indices[scene])
        value.append(count if count>0 else 0.1)  # 用最小值保持边显示
        label_info.append(f"角色：{role}<br>剧情：{scene}<br>台词数量：{count}")
        idx = roles.index(role)
        link_color.append(role_colors[idx % len(role_colors)])

# 剧情→情感
for _, row in scene_emotion.iterrows():
    source.append(node_indices[row['剧情阶段']])
    target.append(node_indices[row['情感分类']])
    value.append(row['count'])
    label_info.append(f"剧情：{row['剧情阶段']}<br>情感：{row['情感分类']}<br>台词数量：{row['count']}")
    link_color.append(emotion_colors_map.get(row['情感分类'], "lightgray"))

# 绘制桑基图
fig = go.Figure(data=[go.Sankey(
    arrangement='snap',
    node=dict(
        pad=15,
        thickness=25,
        line=dict(color="black", width=0.5),
        label=nodes,
        color=role_colors[:len(roles)] + ["orange"]*len(scenes) + [emotion_colors_map.get(e,"lightgray") for e in emotions]
    ),
    link=dict(
        source=source,
        target=target,
        value=value,
        label=label_info,
        color=link_color
    )
)])

fig.update_layout(
    title_text="《甄嬛传》主要角色—剧情—情感桑基图（剧情阶段完整显示）",
    font_size=12
)

fig.show()
