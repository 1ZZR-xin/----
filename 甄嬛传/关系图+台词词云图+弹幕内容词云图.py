

import warnings
from collections import Counter

import jieba
import matplotlib.pyplot as plt
import networkx as nx
from wordcloud import WordCloud

warnings.filterwarnings('ignore')

font_path = '/System/Library/Fonts/PingFang.ttc'
plt.rcParams['font.sans-serif'] = ['PingFang HK', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

# 1. 主要人物关系图
plt.figure(figsize=(16, 12))
G1 = nx.Graph()

relationships = [
    ('甄嬛', '皇上', '夫妻'), ('甄嬛', '果郡王', '真爱'), ('甄嬛', '沈眉庄', '闺蜜'),
    ('甄嬛', '安陵容', '姐妹'), ('甄嬛', '温实初', '青梅竹马'), ('甄嬛', '槿汐', '主仆'),
    ('甄嬛', '浣碧', '主仆'), ('甄嬛', '流朱', '主仆'), ('甄嬛', '华妃', '情敌'),
    ('甄嬛', '皇后', '情敌'), ('甄嬛', '纯元皇后', '替身'), ('甄嬛', '胧月', '母女'),
    ('皇上', '华妃', '宠妃'), ('皇上', '皇后', '夫妻'), ('皇上', '纯元皇后', '白月光'),
    ('皇上', '果郡王', '兄弟'), ('华妃', '年羹尧', '兄妹'), ('华妃', '曹贵人', '主仆'),
    ('皇后', '纯元皇后', '姐妹'), ('皇后', '三阿哥', '母子'), ('皇后', '安陵容', '利用'),
    ('果郡王', '舒太妃', '母子'), ('果郡王', '阿晋', '主仆'), ('沈眉庄', '温实初', '感情'),
    ('安陵容', '皇后', '依附'), ('曹贵人', '温仪公主', '母女'), ('端妃', '华妃', '仇敌')
]

for source, target, relation in relationships:
    G1.add_edge(source, target, label=relation)

pos1 = nx.spring_layout(G1, k=2.5, iterations=50, seed=42)
node_sizes = [4000 if node == '甄嬛' else 3500 if node == '皇上' else 3000 if node in ['华妃', '皇后',
                                                                                       '果郡王'] else 2500 if node in [
    '纯元皇后', '沈眉庄', '安陵容'] else 2000 for node in G1.nodes()]
node_colors = ['#FF69B4' if node == '甄嬛' else '#4169E1' if node == '皇上' else '#FF6347' if node in ['华妃', '皇后',
                                                                                                       '果郡王'] else '#9370DB' if node in [
    '纯元皇后', '沈眉庄', '安陵容'] else '#FFD700' for node in G1.nodes()]

nx.draw_networkx_nodes(G1, pos1, node_size=node_sizes, node_color=node_colors, alpha=0.8)
nx.draw_networkx_edges(G1, pos1, width=1.5, alpha=0.6, edge_color='gray')
nx.draw_networkx_labels(G1, pos1, font_size=10, font_weight='bold', font_family='PingFang HK')

important_edges = [('甄嬛', '皇上'), ('甄嬛', '果郡王'), ('皇上', '华妃'), ('皇上', '皇后'), ('皇后', '纯元皇后'),
                   ('甄嬛', '沈眉庄')]
edge_labels1 = {}
for source, target, relation in relationships:
    if (source, target) in important_edges or (target, source) in important_edges:
        edge_labels1[(source, target)] = relation

nx.draw_networkx_edge_labels(G1, pos1, edge_labels1, font_size=8, font_family='PingFang HK')
plt.title('甄嬛传主要人物关系图', fontsize=20, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()

# 2. 情感关系图
plt.figure(figsize=(14, 10))
G2 = nx.Graph()

love_relationships = [
    ('甄嬛', '皇上', '夫妻'), ('甄嬛', '果郡王', '真爱'), ('皇上', '华妃', '宠幸'),
    ('皇上', '纯元皇后', '深爱'), ('沈眉庄', '温实初', '情愫'), ('果郡王', '浣碧', '情缘'),
    ('皇后', '皇上', '夫妻情')
]

for source, target, relation in love_relationships:
    G2.add_edge(source, target, label=relation)

pos2 = nx.circular_layout(G2)
edge_colors = [
    '#FF1493' if edge in [('甄嬛', '果郡王'), ('果郡王', '甄嬛')] else '#8A2BE2' if edge in [('皇上', '纯元皇后'), (
        '纯元皇后', '皇上')] else '#4169E1' if edge in [('甄嬛', '皇上'), ('皇上', '甄嬛')] else '#FF4500' if edge in [
        ('皇上', '华妃'), ('华妃', '皇上')] else '#32CD32' for edge in G2.edges()]

nx.draw_networkx_nodes(G2, pos2, node_size=3000, node_color='lightblue', alpha=0.8)
nx.draw_networkx_edges(G2, pos2, width=3, alpha=0.7, edge_color=edge_colors)
nx.draw_networkx_labels(G2, pos2, font_size=12, font_weight='bold', font_family='PingFang HK')

edge_labels2 = {edge: relation for source, target, relation in love_relationships for edge in
                [(source, target), (target, source)]}
nx.draw_networkx_edge_labels(G2, pos2, edge_labels2, font_size=10, font_family='PingFang HK')
plt.title('甄嬛传情感关系图', fontsize=18, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()

# 3. 权力关系图
plt.figure(figsize=(14, 10))
G3 = nx.DiGraph()

power_relationships = [
    ('皇上', '皇后', '夫妻'), ('皇上', '华妃', '宠妃'), ('皇上', '甄嬛', '宠妃'),
    ('皇后', '六宫', '管理'), ('华妃', '翊坤宫', '掌管'), ('甄嬛', '永寿宫', '掌管'),
    ('太后', '后宫', '权威'), ('年羹尧', '华妃', '倚仗')
]

for source, target, relation in power_relationships:
    G3.add_edge(source, target, label=relation)

pos3 = nx.spring_layout(G3, k=3, iterations=50, seed=42)
node_colors_power = [
    '#FFD700' if node == '皇上' else '#8B4513' if node == '皇后' else '#DC143C' if node == '华妃' else '#FF69B4' if node == '甄嬛' else '#800080' if node == '太后' else '#708090'
    for node in G3.nodes()]

nx.draw_networkx_nodes(G3, pos3, node_size=2500, node_color=node_colors_power, alpha=0.8)
nx.draw_networkx_edges(G3, pos3, width=2, alpha=0.7, edge_color='gray', arrows=True, arrowsize=20, arrowstyle='->')
nx.draw_networkx_labels(G3, pos3, font_size=11, font_weight='bold', font_family='PingFang HK')
plt.title('甄嬛传权力关系图', fontsize=18, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()

# 4. 台词词云
plt.figure(figsize=(12, 8))
script_text = """
甄嬛:槿汐,让我看看。槿汐这孔雀开屏栩栩如生,真好看。流朱:是!槿汐:哪里比得上小主的和合二仙呢?
甄嬛:自到宫中,人人都求皇恩盛宠,我一愿父母妹妹安康顺遂,二愿在宫中平安一世,了此残生。
甄嬛:愿"逆风如解意,容易莫摧残" 皇帝:谁在那里?是谁在那里?是谁?
甄嬛:奴婢倚梅园的宫女,不想扰了尊驾,请恕罪。皇帝:你读过书吗?叫什么名字?
华妃:皇上用过膳了吗?臣妾宫中来了位新厨子,做得一手江南好菜。
眉庄:皇上,臣妾冤枉,臣妾真的冤枉。甄嬛:皇上,臣妾与姐姐一同长大,姐姐是何为人臣妾再清楚不过了。
华妃:胆子还挺大的，冷宫也敢这样进来 甄嬛:这个地方我来的比你多
华妃:你不要做梦了，你把我害到如此地步，我做鬼都不会放过你
甄嬛:没有人要害你，是你自作自受，淳贵人溺水是你做的吧
华妃:皇上，你害得世兰好苦啊 甄嬛:寄予宛宛爱妻，念悲去，独余斯良苦此身，常自魂牵梦萦，忧思难忘，纵得菀菀，菀菀类卿
皇上:其实能有几分像菀莞，也算是你的福气。甄嬛:是吗?究竟是我的福还是我的孽?
甄嬛:这几年的情爱与时光，究竟是错付了。允礼:嬛儿,我不是和你开玩笑。
甄嬛:可我只能当您是玩笑。允礼:从前你是皇上的女人,现在已是自由之身!
允礼:嬛儿,在我心里,你就是我的天地人间。皇后:皇上,臣妾做不到啊!
祺贵人:臣妾要告发熹贵妃私通秽乱后宫 静白:贫尼甘露寺静白见过皇上，皇后娘娘。
"""

words = jieba.lcut(script_text)
stop_words = {'的', '了', '啊', '呢', '吧', '吗', '是', '在', '和', '与', '之', '其', '这', '那', '我', '你', '他',
              '她', '臣妾', '皇上', '娘娘', '奴婢', '小主', '臣', '本宫', '哀家', '朕', '贵人', '嫔妾', '什么', '怎么',
              '不是', '就是', '也', '都', '来', '去', '给', '把', '让', '被', '要', '会', '能', '可以', '说', '看',
              '想', '知道'}
filtered_words = [word for word in words if len(word) > 1 and word not in stop_words]
word_freq = Counter(filtered_words)

wordcloud1 = WordCloud(width=800, height=600, background_color='white', max_words=100, colormap='viridis',
                       font_path=font_path).generate_from_frequencies(word_freq)
plt.imshow(wordcloud1, interpolation='bilinear')
plt.axis('off')
plt.title('甄嬛传台词关键词云', fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

# 5. 人物出现频率词云
plt.figure(figsize=(12, 8))
character_freq = {
    '甄嬛': 25, '皇上': 20, '华妃': 15, '皇后': 18, '沈眉庄': 12, '安陵容': 10,
    '果郡王': 14, '温实初': 8, '曹贵人': 6, '端妃': 5, '敬妃': 5, '齐妃': 4,
    '富察贵人': 3, '淳贵人': 3, '祺贵人': 4, '纯元皇后': 8, '舒太妃': 3,
    '胧月': 6, '四阿哥': 5
}

wordcloud2 = WordCloud(width=800, height=600, background_color='white', max_words=50, colormap='plasma',
                       font_path=font_path,
                       prefer_horizontal=0.9, relative_scaling=0.5).generate_from_frequencies(character_freq)
plt.imshow(wordcloud2, interpolation='bilinear')
plt.axis('off')
plt.title('甄嬛传人物出现频率词云', fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

# 6. 关键场景词云
plt.figure(figsize=(12, 8))
scene_freq = {
    '倚梅园': 15, '碎玉轩': 12, '翊坤宫': 10, '永寿宫': 8, '景仁宫': 6, '闲月阁': 5,
    '甘露寺': 14, '凌云峰': 10, '清凉台': 8, '养心殿': 7, '寿康宫': 5, '交芦馆': 4,
    '逆风如解意': 12, '莞莞类卿': 10, '滴血验亲': 8, '假孕争宠': 7, '纯元故衣': 6,
    '欢宜香': 9, '长相思': 8, '长相守': 7, '皇后杀了皇后': 6
}

wordcloud3 = WordCloud(width=800, height=600, background_color='white', max_words=30, colormap='coolwarm',
                       font_path=font_path, prefer_horizontal=0.9, relative_scaling=0.5).generate_from_frequencies(
    scene_freq)
plt.imshow(wordcloud3, interpolation='bilinear')
plt.axis('off')
plt.title('甄嬛传关键场景词云', fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

# 7. 阵营关系图
plt.figure(figsize=(14, 10))
G5 = nx.Graph()

faction_relationships = [
    ('甄嬛', '沈眉庄', 1), ('甄嬛', '槿汐', 1), ('甄嬛', '浣碧', 1), ('甄嬛', '流朱', 1), ('甄嬛', '温实初', 1),
    ('沈眉庄', '温实初', 1),
    ('华妃', '曹贵人', 1), ('华妃', '颂芝', 1), ('华妃', '周宁海', 1), ('曹贵人', '温仪公主', 1),
    ('皇后', '安陵容', 1), ('皇后', '剪秋', 1), ('皇后', '江福海', 1), ('皇后', '三阿哥', 1),
    ('皇上', '甄嬛', 0), ('皇上', '华妃', 0), ('皇上', '皇后', 0), ('果郡王', '舒太妃', 1), ('果郡王', '阿晋', 1),
    ('纯元皇后', '皇上', 0)
]

for source, target, faction in faction_relationships:
    G5.add_edge(source, target, faction=faction)

pos5 = nx.spring_layout(G5, k=3, iterations=50, seed=42)
node_colors_faction = [
    '#FF69B4' if node in ['甄嬛', '沈眉庄', '槿汐', '浣碧', '流朱', '温实初'] else '#FF4500' if node in ['华妃',
                                                                                                         '曹贵人',
                                                                                                         '颂芝',
                                                                                                         '周宁海',
                                                                                                         '温仪公主'] else '#800080' if node in [
        '皇后', '安陵容', '剪秋', '江福海', '三阿哥'] else '#FFD700' if node == '皇上' else '#32CD32' if node in [
        '果郡王', '舒太妃', '阿晋'] else '#87CEEB' if node == '纯元皇后' else '#708090' for node in G5.nodes()]

nx.draw_networkx_nodes(G5, pos5, node_size=2500, node_color=node_colors_faction, alpha=0.8)
nx.draw_networkx_edges(G5, pos5, width=2, alpha=0.6, edge_color='gray')
nx.draw_networkx_labels(G5, pos5, font_size=10, font_weight='bold', font_family='PingFang HK')

from matplotlib.patches import Patch

legend_elements = [Patch(facecolor='#FF69B4', label='甄嬛阵营'), Patch(facecolor='#FF4500', label='华妃阵营'),
                   Patch(facecolor='#800080', label='皇后阵营'), Patch(facecolor='#FFD700', label='皇帝'),
                   Patch(facecolor='#32CD32', label='果郡王阵营'), Patch(facecolor='#87CEEB', label='纯元皇后')]
plt.legend(handles=legend_elements, loc='upper right', fontsize=10)
plt.title('甄嬛传阵营关系图', fontsize=18, fontweight='bold', pad=20)
plt.axis('off')
plt.tight_layout()
plt.show()

# 8. 时间线关系图
fig, axes = plt.subplots(1, 3, figsize=(18, 6))
fig.suptitle('甄嬛传时间线人物关系演变', fontsize=20, weight='bold')

timeline_data = {
    '初期': {'nodes': ['甄嬛', '皇上', '华妃', '皇后', '沈眉庄', '安陵容'],
             'edges': [('甄嬛', '皇上'), ('甄嬛', '沈眉庄'), ('华妃', '皇上'), ('皇后', '皇上')]},
    '中期': {'nodes': ['甄嬛', '皇上', '华妃', '皇后', '果郡王', '温实初'],
             'edges': [('甄嬛', '皇上'), ('甄嬛', '果郡王'), ('华妃', '皇上'), ('皇后', '皇上')]},
    '后期': {'nodes': ['甄嬛', '皇上', '皇后', '果郡王', '四阿哥', '胧月'],
             'edges': [('甄嬛', '皇上'), ('甄嬛', '果郡王'), ('甄嬛', '四阿哥'), ('皇后', '皇上')]}
}

for i, (period, data) in enumerate(timeline_data.items()):
    ax = axes[i]
    G = nx.Graph()
    G.add_nodes_from(data['nodes'])
    G.add_edges_from(data['edges'])
    pos = nx.spring_layout(G, k=2, iterations=20, seed=42)

    node_colors = ['#FF69B4' if node == '甄嬛' else '#4169E1' if node == '皇上' else '#FF6347' if node in ['华妃',
                                                                                                           '皇后'] else '#32CD32' if node == '果郡王' else '#FFD700'
                   for node in G.nodes()]

    nx.draw_networkx_nodes(G, pos, node_size=800, node_color=node_colors, alpha=0.8, ax=ax)
    nx.draw_networkx_edges(G, pos, width=2, alpha=0.6, edge_color='gray', ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=9, font_weight='bold', font_family='PingFang HK', ax=ax)

    ax.set_title(f'{period}关系', fontsize=14, weight='bold')
    ax.axis('off')

plt.tight_layout()
plt.show()

# 9. 情感词汇云
plt.figure(figsize=(12, 8))
emotion_freq = {
    '爱情': 20, '深情': 15, '真心': 12, '宠爱': 10, '痴情': 8, '相思': 14, '思念': 10,
    '等待': 8, '守护': 9, '牵挂': 7, '心动': 6, '喜欢': 8, '仇恨': 12, '怨恨': 10,
    '嫉妒': 9, '妒忌': 7, '愤怒': 8, '报复': 6, '陷害': 7, '背叛': 8, '友情': 15,
    '闺蜜': 12, '姐妹': 10, '忠诚': 8, '信任': 9, '陪伴': 7, '亲情': 11, '母子': 9,
    '家人': 8, '关爱': 7, '权力': 13, '地位': 10, '宠幸': 8, '尊贵': 7, '权威': 6, '命运': 9
}

wordcloud4 = WordCloud(width=800, height=600, background_color='white', max_words=40, colormap='RdYlBu',
                       font_path=font_path,
                       prefer_horizontal=0.9, relative_scaling=0.5).generate_from_frequencies(emotion_freq)
plt.imshow(wordcloud4, interpolation='bilinear')
plt.axis('off')
plt.title('甄嬛传情感词汇云', fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

# 10. 经典台词词云
plt.figure(figsize=(12, 8))
classic_lines = {
    '逆风如解意': 10, '容易莫摧残': 8, '莞莞类卿': 9, '臣妾做不到': 8, '皇上你害得世兰好苦': 7,
    '皇后杀了皇后': 8, '滴血验亲': 7, '假孕争宠': 6, '纯元故衣': 6, '欢宜香': 7,
    '长相思': 6, '长相守': 6, '碎玉轩': 5, '倚梅园': 5, '翊坤宫': 5, '永寿宫': 5,
    '甘露寺': 6, '凌云峰': 5, '清凉台': 4, '养心殿': 4
}

wordcloud5 = WordCloud(width=800, height=600, background_color='white', max_words=25, colormap='plasma',
                       font_path=font_path,
                       prefer_horizontal=0.9, relative_scaling=0.7).generate_from_frequencies(classic_lines)
plt.imshow(wordcloud5, interpolation='bilinear')
plt.axis('off')
plt.title('甄嬛传经典台词词云', fontsize=16, weight='bold')
plt.tight_layout()
plt.show()

import pandas as pd
from snownlp import SnowNLP

# 1. 读取数据
print("正在读取数据...")
df = pd.read_csv('./莞莞类卿-纯元故衣事件.csv', encoding='utf-8-sig')


# 2. 情感分析函数
def get_sentiment(text):
    try:
        return SnowNLP(text).sentiments
    except:
        return 0.5


print("正在进行情感分析...")
df['情感得分'] = df['弹幕内容'].apply(get_sentiment)


# 3. 情感分类
def classify_sentiment(score):
    if score > 0.6:
        return '积极'
    elif score < 0.4:
        return '消极'
    else:
        return '中性'


df['情感分类'] = df['情感得分'].apply(classify_sentiment)

# 4. 创建可视化图表
print("生成可视化图表...")
fig = plt.figure(figsize=(18, 12))

# 图1: 情感分布饼图
ax1 = plt.subplot(2, 3, 1)
sentiment_counts = df['情感分类'].value_counts()
colors = ['#4CAF50', '#FFC107', '#F44336']  # 绿, 黄, 红
ax1.pie(sentiment_counts.values, labels=sentiment_counts.index, autopct='%1.1f%%',
        colors=colors, startangle=90)
ax1.set_title('弹幕情感分布', fontsize=14, fontweight='bold')
ax1.axis('equal')

# 图2: 情感得分分布直方图
ax2 = plt.subplot(2, 3, 2)
ax2.hist(df['情感得分'], bins=30, color='skyblue', edgecolor='black', alpha=0.7)
ax2.axvline(x=df['情感得分'].mean(), color='red', linestyle='--', linewidth=2,
            label=f'平均值: {df["情感得分"].mean():.3f}')
ax2.set_xlabel('情感得分 (0-1)', fontsize=12)
ax2.set_ylabel('频数', fontsize=12)
ax2.set_title('情感得分分布直方图', fontsize=14, fontweight='bold')
ax2.legend()
ax2.grid(True, alpha=0.3)

# 图3: 不同情感类别的箱线图
ax3 = plt.subplot(2, 3, 3)
sentiment_data = [df[df['情感分类'] == cat]['情感得分'] for cat in ['积极', '中性', '消极']]
ax3.boxplot(sentiment_data, labels=['积极', '中性', '消极'], patch_artist=True,
            boxprops=dict(facecolor='lightblue'))
ax3.set_ylabel('情感得分', fontsize=12)
ax3.set_title('不同情感类别的得分分布', fontsize=14, fontweight='bold')
ax3.grid(True, alpha=0.3)

# 图4: 按时间的情感变化趋势
ax4 = plt.subplot(2, 3, 4)
df['出现时间秒'] = pd.to_numeric(df['出现时间秒'], errors='coerce')
# 按时间窗口平滑处理
window_size = 20
df_sorted = df.sort_values('出现时间秒')
df_sorted['情感得分平滑'] = df_sorted['情感得分'].rolling(window=window_size, center=True).mean()
ax4.scatter(df_sorted['出现时间秒'], df_sorted['情感得分'], alpha=0.3, s=10, color='gray')
ax4.plot(df_sorted['出现时间秒'], df_sorted['情感得分平滑'], color='red', linewidth=2)
ax4.set_xlabel('视频时间 (秒)', fontsize=12)
ax4.set_ylabel('情感得分', fontsize=12)
ax4.set_title(f'情感得分随时间变化趋势 (滑动窗口: {window_size}条)', fontsize=14, fontweight='bold')
ax4.grid(True, alpha=0.3)

# 图5: 弹幕长度与情感关系
ax5 = plt.subplot(2, 3, 5)
df['弹幕长度'] = df['弹幕内容'].str.len()
scatter = ax5.scatter(df['弹幕长度'], df['情感得分'],
                      c=df['情感得分'], cmap='RdYlGn', alpha=0.6, edgecolors='black', linewidth=0.5)
ax5.set_xlabel('弹幕长度 (字符数)', fontsize=12)
ax5.set_ylabel('情感得分', fontsize=12)
ax5.set_title('弹幕长度与情感得分关系', fontsize=14, fontweight='bold')
plt.colorbar(scatter, ax=ax5)
ax5.grid(True, alpha=0.3)

# 图6: 高频词汇分析
ax6 = plt.subplot(2, 3, 6)
# 提取所有弹幕文本
all_text = ' '.join(df['弹幕内容'].astype(str).tolist())
# 分词并过滤停用词
words = jieba.lcut(all_text)
stopwords = ['的', '了', '在', '是', '我', '你', '他', '她', '它', '这', '那', '和', '与',
             '就', '都', '而', '及', '等', '们', '也', '着', '个', '来', '去', '说', '要',
             '不', '吗', '啊', '呢', '吧', '哦', '嗯', '唉', '哇', '哈', '哈哈哈']
words_filtered = [word for word in words if len(word) > 1 and word not in stopwords]
# 统计词频
word_counts = Counter(words_filtered).most_common(15)
words_top = [item[0] for item in word_counts][::-1]
counts_top = [item[1] for item in word_counts][::-1]
ax6.barh(words_top, counts_top, color='steelblue')
ax6.set_xlabel('出现次数', fontsize=12)
ax6.set_title('高频词汇TOP15', fontsize=14, fontweight='bold')
ax6.grid(True, alpha=0.3, axis='x')

plt.suptitle('《甄嬛传》"莞莞类卿"情节弹幕情感分析', fontsize=18, fontweight='bold', y=0.98)
plt.tight_layout()
plt.show()

# 7. 生成词云图
print("\n生成词云图...")
fig2 = plt.figure(figsize=(12, 8))
# 生成词云
wordcloud = WordCloud(
    font_path=font_path,  # 可以使用系统中文字体路径
    width=800,
    height=600,
    background_color='white',
    max_words=200,
    max_font_size=100,
    random_state=42,
    colormap='viridis'
).generate(' '.join(words_filtered))

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.title('弹幕内容词云图', fontsize=16, fontweight='bold', pad=20)
plt.tight_layout()
plt.show()

# 8. 打印统计摘要
print("\n" + "=" * 60)
print("情感分析统计摘要")
print("=" * 60)
print(f"总弹幕数: {len(df)} 条")
print(f"平均情感得分: {df['情感得分'].mean():.3f}")
print(f"情感得分中位数: {df['情感得分'].median():.3f}")
print(f"情感得分标准差: {df['情感得分'].std():.3f}")
print("\n情感分类统计:")
for sentiment, count in sentiment_counts.items():
    percentage = count / len(df) * 100
    print(f"  {sentiment}: {count} 条 ({percentage:.1f}%)")

print("\n情感得分范围:")
print(f"  最低: {df['情感得分'].min():.3f}")
print(f"  最高: {df['情感得分'].max():.3f}")
print(f"  25%分位数: {df['情感得分'].quantile(0.25):.3f}")
print(f"  75%分位数: {df['情感得分'].quantile(0.75):.3f}")

# 9. 情感分析示例
print("\n" + "=" * 60)
print("情感分析示例")
print("=" * 60)
print("积极弹幕示例 (得分>0.8):")
positive_examples = df[df['情感得分'] > 0.8].head(3)
for _, row in positive_examples.iterrows():
    print(f"  ✓ [{row['情感得分']:.3f}] {row['弹幕内容'][:50]}...")

print("\n消极弹幕示例 (得分<0.2):")
negative_examples = df[df['情感得分'] < 0.2].head(3)
for _, row in negative_examples.iterrows():
    print(f"  ✗ [{row['情感得分']:.3f}] {row['弹幕内容'][:50]}...")




