import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import jieba
from collections import Counter
import warnings

warnings.filterwarnings('ignore')

plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei']
plt.rcParams['axes.unicode_minus'] = False


def analyze_dialogue_sentiment(file_path, stage_name):
    print(f"\n正在分析：{stage_name}")

    # ===== 读取 CSV（自动编码）=====
    try:
        df = pd.read_csv(file_path, encoding='utf-8-sig')
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding='gbk')

    print("当前 CSV 列名：", df.columns.tolist())

    # ===== 自动识别列名 =====
    dialogue_candidates = ['dialogue', '台词', '对白', '内容', '文本']
    speaker_candidates = ['speaker', '人物', '角色', '说话人']

    dialogue_col = None
    speaker_col = None

    for col in dialogue_candidates:
        if col in df.columns:
            dialogue_col = col
            break

    for col in speaker_candidates:
        if col in df.columns:
            speaker_col = col
            break

    if dialogue_col is None:
        raise ValueError("❌ 未找到台词列，请检查 CSV")

    if speaker_col is None:
        raise ValueError("❌ 未找到人物列，请检查 CSV")

    print(f"✔ 台词列：{dialogue_col} | 人物列：{speaker_col}")

    # ===== 情感分析 =====
    def get_sentiment(text):
        try:
            return SnowNLP(str(text)).sentiments
        except:
            return 0.5

    df['情感得分'] = df[dialogue_col].apply(get_sentiment)

    def classify_sentiment(score):
        if score > 0.6:
            return '积极'
        elif score < 0.4:
            return '消极'
        else:
            return '中性'

    df['情感分类'] = df['情感得分'].apply(classify_sentiment)

    # ===== 可视化 =====
    plt.figure(figsize=(12, 8))

    # 情感分布
    plt.subplot(2, 2, 1)
    df['情感分类'].value_counts().plot.pie(autopct='%1.1f%%')
    plt.title(f'{stage_name} 台词情感分布')

    # 情感得分分布
    plt.subplot(2, 2, 2)
    plt.hist(df['情感得分'], bins=30)
    plt.title('情感得分分布')

    # 人物情感对比
    plt.subplot(2, 2, 3)
    (
        df.groupby(speaker_col)['情感得分']
        .mean()
        .sort_values(ascending=False)
        .head(8)
        .plot(kind='bar')
    )
    plt.title('主要人物平均情感得分')

    # 高频词
    plt.subplot(2, 2, 4)
    text = ' '.join(df[dialogue_col].astype(str))
    words = jieba.lcut(text)
    stopwords = ['的','了','在','是','我','你','他','她','这','那','也']
    words = [w for w in words if len(w) > 1 and w not in stopwords]
    top_words = Counter(words).most_common(10)

    if top_words:
        words_top, counts = zip(*top_words)
        plt.barh(words_top[::-1], counts[::-1])
    plt.title('高频词 TOP10')

    plt.suptitle(stage_name, fontsize=14)
    plt.tight_layout()
    plt.show()

    # ===== 保存结果 =====
    output_name = f"{stage_name}_台词_情感分析.csv"
    df['人物'] = df[speaker_col]
    df['台词'] = df[dialogue_col]
    df.to_csv(output_name, index=False, encoding='utf-8-sig')
    print(f"✅ 已生成：{output_name}")

    return df[['人物', '台词', '情感得分', '情感分类']]


# ===== 九个关键情节 =====
files = [
    ("一.csv", "初入宫廷"),
    ("二.csv", "眉庄受害"),
    ("三.csv", "华妃之死"),
    ("四.csv", "首次小产"),
    ("五.csv", "莞莞类卿"),
    ("六.csv", "出宫与定情"),
    ("七.csv", "回宫反转"),
    ("八.csv", "滴血验亲"),
    ("九.csv", "真相揭晓")
]

all_data = []

for f, name in files:
    df_stage = analyze_dialogue_sentiment(f, name)
    df_stage['剧情阶段'] = name
    all_data.append(df_stage)

# ===== 合并总表（语义网络用）=====
all_df = pd.concat(all_data, ignore_index=True)
all_df.to_csv("全剧_台词_情感汇总.csv", index=False, encoding='utf-8-sig')

print("\n🎯 已生成：全剧_台词_情感汇总.csv（用于语义网络 / 知识图谱）")
