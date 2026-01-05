import pandas as pd
from snownlp import SnowNLP
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
import jieba
from collections import Counter
import warnings
import os


def analyze_danmu_sentiment(file_path):
    """
    对弹幕数据进行情感分析并生成可视化报告

    参数:
    file_path (str): CSV文件路径
    """
    warnings.filterwarnings('ignore')

    # 设置中文字体
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'Arial']
    plt.rcParams['axes.unicode_minus'] = False
    plt.rcParams['font.sans-serif'] = ['SimHei']  # Windows
    # 1. 读取数据
    print("正在读取数据...")
    df = pd.read_csv(file_path, encoding='utf-8-sig')

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

    plt.suptitle('弹幕情感分析', fontsize=18, fontweight='bold', y=0.98)
    plt.tight_layout()
    plt.show()

    # 自动检测字体路径
    font_paths = [
        '/System/Library/Fonts/PingFang.ttc',  # macOS
        'C:/Windows/Fonts/simhei.ttf',  # Windows
        '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',  # Linux
        'simhei.ttf'  # 当前目录
    ]

    font_path = None
    for path in font_paths:
        if os.path.exists(path):
            font_path = path
            break

    if font_path is None:
        print("警告: 未找到中文字体，词云可能无法正常显示中文")
        font_path = None

    # 7. 生成词云图
    print("\n生成词云图...")
    fig2 = plt.figure(figsize=(12, 8))
    # 生成词云
    wordcloud = WordCloud(
        font_path=font_path,
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


analyze_danmu_sentiment('./莞莞类卿-纯元故衣事件.csv')
analyze_danmu_sentiment('./华妃之死-皇上你害得世兰好苦啊.csv')
analyze_danmu_sentiment('./沈眉庄被陷害假孕争宠.csv')
analyze_danmu_sentiment('./滴血验亲.csv')
analyze_danmu_sentiment('./甄嬛设计与皇上重逢，风光回宫.csv')
analyze_danmu_sentiment('./甄嬛逆风如解意与皇上御花园初遇.csv')
analyze_danmu_sentiment('./甄嬛首次小产（被猫抓伤后遭安陵容暗算）.csv')
analyze_danmu_sentiment('./皇后杀了皇后-纯元皇后死亡真相揭晓.csv')
