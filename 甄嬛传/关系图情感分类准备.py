import pandas as pd
from snownlp import SnowNLP

# 1. 读取 CSV
df = pd.read_csv("test.csv", encoding="utf-8-sig")

# 2. 定义情感分析函数
def get_sentiment(text):
    try:
        return SnowNLP(str(text)).sentiments
    except:
        return 0.5

# 3. 定义情感分类规则
def classify_sentiment(score):
    if score > 0.6:
        return "积极"
    elif score < 0.4:
        return "消极"
    else:
        return "中性"

# 4. ★真正“加列”的两行（你问的那两行）
df["情感得分"] = df["dialogue"].apply(get_sentiment)
df["情感分类"] = df["情感得分"].apply(classify_sentiment)

# 5. 保存新 CSV
df.to_csv("test_情感分析后.csv", index=False, encoding="utf-8-sig")

print("✅ 已生成：test_情感分析后.csv")
print(df.head())
