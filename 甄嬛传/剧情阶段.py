def analyze_dialogue_sentiment(file_path, stage_name):
    df = pd.read_csv(file_path, encoding='utf-8-sig')

    # 如果没有情感分类，就生成
    if '情感分类' not in df.columns:
        def classify(score):
            if score > 0.6:
                return '积极'
            elif score < 0.4:
                return '消极'
            else:
                return '中性'
        df['情感分类'] = df['情感得分'].apply(classify)

    # ⭐关键：补剧情阶段
    df['剧情阶段'] = stage_name

    return df
