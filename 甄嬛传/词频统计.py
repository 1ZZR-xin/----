import re
from collections import Counter
import os

# 《甄嬛传》角色名和关键词列表
zhuanhuan_keywords = {
    '甄嬛', '皇上', '华妃', '皇后', '果郡王', '允礼', '沈眉庄', '安陵容',
    '温实初', '浣碧', '槿汐', '苏培盛', '纯元', '宜修', '年世兰', '祺贵人',
    '敬妃', '端妃', '曹贵人', '齐妃', '欣常在', '富察贵人', '贞嫔', '康常在',
    '隆科多', '太后', '舒太妃', '莫言', '静白', '斐雯', '剪秋', '颂芝',
    '周宁海', '刘畚', '茯苓', '江诚', '章弥', '采月', '采蓝', '采蘋',
    '阿晋', '积云', '孟静娴', '沛国公', '胧月', '弘历', '三阿哥',
    '碎玉轩', '翊坤宫', '闲月阁', '永寿宫', '清凉台', '甘露寺', '凌云峰',
    '倚梅园', '寿康宫', '景仁宫', '养心殿', '安棲观',
    '滴血验亲', '莞莞类卿', '逆风如解意', '假孕争宠', '欢宜香', '长相思',
    '长相守', '和合二仙', '玉蕊檀心梅', '麝香', '红花', '桃仁', '杏仁茶',
    '芭蕉', '龙涎香', '东阿阿胶桂圆羹', '莞贵人', '惠贵人', '熹妃', '惠嫔',
    '莞嫔', '年答应', '沈贵人', '眉庄', '陵容', '世兰', '嬛儿', '嬛嬛',
    '四郎', '王爷', '小主', '娘娘', '太后', '太妃', '太医', '皇帝', '皇上',
    '朕', '臣妾', '嫔妾', '奴婢', '奴才', '本宫', '皇上', '贵妃', '贵妃娘娘',
    '莞嫔', '惠嫔', '安常在', '曹琴默', '襄嫔', '年氏', '年羹尧', '甄伯父',
    '甄父', '甄大人', '刘太医', '江太医', '温太医', '章太医', '太医',
    '皇兄', '皇弟', '皇子', '皇嗣', '龙裔', '龙胎', '皇子', '胧月公主',
    '四阿哥', '三阿哥', '太子', '储君', '福晋', '侧福晋', '嫡福晋', '庶出',
    '嫡出', '嫡子', '庶子', '嫡女', '庶女'
}

# 情感词列表（优化版）
emotion_words = {
    '爱', '恨', '苦', '痛', '泪', '哭', '笑', '喜', '怒', '悲', '欢',
    '怨', '痴', '毒', '狠', '惨', '虐', '酸', '甜', '怕', '惊', '忧',
    '愁', '思', '念', '悔', '愧', '羞', '耻', '骄', '傲', '狂', '妄',
    '奸', '诈', '阴', '险', '恶', '善', '美', '丑', '真', '假', '虚',
    '实', '生', '死', '病', '伤', '残', '废', '疯', '傻', '痴', '呆',
    '冤', '枉', '屈', '辱', '宠', '幸', '宠幸', '失宠', '争宠', '专宠',
    '盛宠', '恩宠', '荣宠', '冷落', '嫌弃', '厌恶', '讨厌', '喜欢',
    '喜爱', '疼爱', '宠爱', '心疼', '心痛', '心碎', '心酸', '心寒',
    '心凉', '心死', '伤心', '开心', '担心', '关心', '痛心', '寒心',
    '凉心', '死心', '动心', '惊心', '慌心', '颤心', '跳心', '爱心',
    '恨心', '喜心', '怒心', '悲心', '欢心', '怨心', '痴心', '狠心',
    '毒心', '机心', '思心', '意心', '情心', '绪心', '态心', '灵心',
    '可怜', '可恨', '可怕', '可爱', '可亲', '可敬', '可恶', '可耻',
    '可悲', '可喜', '可贺', '可笑', '可叹', '可惜', '可气', '愤怒',
    '生气', '高兴', '快乐', '幸福', '悲伤', '痛苦', '难过', '伤心',
    '开心', '兴奋', '激动', '平静', '冷漠', '热情', '冷淡', '温柔',
    '凶狠', '善良', '邪恶', '正直', '奸诈', '忠诚', '背叛', '信任',
    '怀疑', '相信', '不信', '希望', '失望', '绝望', '期望', '盼望',
    '渴望', '祈求', '祈祷', '祝福', '诅咒', '赞美', '批评', '表扬',
    '责备', '责怪', '埋怨', '抱怨', '感激', '感谢', '感动', '感慨',
    '感叹', '叹息', '害怕', '恐惧', '惊慌', '慌张', '慌乱', '惊恐',
    '惊吓', '恐惧', '可怕', '害怕', '惊吓', '恐惧', '害怕', '惊慌'
}

# 停用词列表（扩展版）
stop_words = {
    '的', '了', '在', '是', '有', '和', '与', '及', '或', '但', '而',
    '且', '又', '也', '都', '就', '却', '这', '那', '哪', '谁', '什么',
    '怎么', '为什么', '如何', '怎样', '因为', '所以', '虽然', '但是',
    '如果', '那么', '不仅', '而且', '既然', '那么', '即使', '也',
    '无论', '都', '只有', '才', '只要', '就', '除非', '否则', '一边',
    '一边', '一面', '一面', '既', '又', '不但', '还', '尽管', '还是',
    '不管', '都', '之所以', '是因为', '由于', '因此', '因而', '于是',
    '然后', '接着', '最后', '首先', '其次', '再次', '最后', '总之',
    '总而言之', '例如', '比如', '譬如', '诸如', '等等', '等', '之类',
    '之一', '之二', '之三', '之上', '之下', '之前', '之后', '之中',
    '之内', '之外', '之间', '一个', '一些', '一点', '有些', '有点',
    '很多', '很少', '许多', '大量', '少量', '全部', '部分', '整体',
    '局部', '个别', '一般', '特殊', '特别', '普通', '平常', '正常',
    '异常', '反常', '奇怪', '奇妙', '神奇', '神秘', '神圣', '庄严',
    '严肃', '严厉', '严格', '严谨', '严密', '紧密', '密切', '亲密',
    '亲近', '亲切', '亲热', '热情', '热心', '热忱', '热烈', '热闹',
    '人', '事', '物', '东西', '地方', '时候', '时间', '地点', '原因',
    '结果', '过程', '方法', '方式', '手段', '工具', '材料', '资源',
    '条件', '环境', '情况', '状态', '形势', '局面', '场面', '情景',
    '景象', '现象', '事实', '真相', '假象', '表象', '本质', '实质',
    '核心', '关键', '重点', '要点', '难点', '疑点', '焦点', '热点',
    '亮点', '暗点', '优点', '缺点', '长处', '短处', '优势', '劣势',
    '机会', '威胁', '风险', '危机', '机遇', '挑战', '竞争', '合作',
    '冲突', '矛盾', '纠纷', '争议', '争论', '辩论', '讨论', '交流',
    '沟通', '对话', '谈判', '协商', '妥协', '让步', '坚持', '放弃',
    '改变', '调整', '改进', '改善', '提高', '提升', '降低', '减少',
    '增加', '增强', '减弱', '加强', '削弱', '巩固', '稳定', '动摇',
    '崩溃', '瓦解', '分裂', '统一', '整合', '融合', '分离', '分开',
    '结合', '联合', '合作', '协作', '配合', '协调', '调节', '调整'
}

class FastChineseSegmenter:
    """高效中文分词器"""
    
    def __init__(self):
        # 构建词典树
        self.trie = {}
        self.max_word_len = 0
        
        # 添加所有关键词到词典树
        all_keywords = zhuanhuan_keywords.union(emotion_words)
        for word in all_keywords:
            self._add_word(word)
            self.max_word_len = max(self.max_word_len, len(word))
        
        print(f"词典加载完成，最大词长: {self.max_word_len}，总词数: {len(all_keywords)}")
    
    def _add_word(self, word):
        """添加词到Trie树"""
        node = self.trie
        for char in word:
            if char not in node:
                node[char] = {}
            node = node[char]
        node['#'] = True  # 标记词尾
    
    def fast_segment(self, text):
        """快速分词 - 使用Trie树和滑动窗口"""
        words = []
        i = 0
        n = len(text)
        
        while i < n:
            # 跳过非中文字符
            if not ('\u4e00' <= text[i] <= '\u9fff'):
                i += 1
                continue
            
            # 查找最长匹配
            matched_word = None
            matched_len = 0
            node = self.trie
            current_word = ""
            
            # 查找最长匹配词
            for j in range(i, min(i + self.max_word_len, n)):
                char = text[j]
                if char not in node:
                    break
                node = node[char]
                current_word += char
                if '#' in node:  # 找到完整词
                    matched_word = current_word
                    matched_len = j - i + 1
            
            if matched_word:
                words.append(matched_word)
                i += matched_len
            else:
                # 单字处理
                if text[i] not in stop_words:
                    words.append(text[i])
                i += 1
        
        return words
    
    def batch_segment(self, texts, batch_size=1000):
        """批量分词"""
        all_words = []
        for i in range(0, len(texts), batch_size):
            batch = texts[i:i+batch_size]
            for text in batch:
                words = self.fast_segment(text)
                all_words.extend(words)
        return all_words

def clean_text_fast(text):
    """快速清理文本"""
    # 使用更高效的正则表达式
    text = re.sub(r'[\(（].*?[）\)]', '', text, flags=re.DOTALL)
    text = re.sub(r'[0-9a-zA-Z]', '', text)
    text = re.sub(r'[，。！？；："「」『』《》【】、]', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def process_large_text(text, chunk_size=10000):
    """分块处理大文本"""
    print(f"文本大小: {len(text):,} 字符")
    print("正在分块处理...")
    
    # 按句子或段落分块
    chunks = []
    current_chunk = ""
    
    # 简单按标点分块
    sentences = re.split(r'[。！？；\n]', text)
    
    for sentence in sentences:
        sentence = sentence.strip()
        if not sentence:
            continue
        
        if len(current_chunk) + len(sentence) < chunk_size:
            current_chunk += sentence + "。"
        else:
            if current_chunk:
                chunks.append(current_chunk)
            current_chunk = sentence + "。"
    
    if current_chunk:
        chunks.append(current_chunk)
    
    print(f"分块完成: {len(chunks)} 个块")
    return chunks

def analyze_large_text(text, scene_name="弹幕分析", top_n=100):
    """分析大文本（优化版）"""
    print(f"\n{'='*60}")
    print(f"分析场景: {scene_name}")
    print(f"{'='*60}")
    
    # 1. 清理文本
    print("1. 清理文本...")
    cleaned_text = clean_text_fast(text)
    print(f"   清理后长度: {len(cleaned_text):,} 字符")
    
    if len(cleaned_text) < 10:
        print("文本太短，无法分析")
        return None
    
    # 2. 分块处理
    print("2. 分块处理...")
    chunks = process_large_text(cleaned_text)
    
    # 3. 初始化分词器
    print("3. 初始化分词器...")
    segmenter = FastChineseSegmenter()
    
    # 4. 批量分词
    print("4. 批量分词...")
    start_time = time.time()
    
    all_words = []
    total_chunks = len(chunks)
    
    for i, chunk in enumerate(chunks):
        words = segmenter.fast_segment(chunk)
        all_words.extend(words)
        
        # 显示进度
        if total_chunks > 10 and i % (total_chunks // 10) == 0:
            progress = (i + 1) / total_chunks * 100
            print(f"   分词进度: {progress:.1f}% ({i+1}/{total_chunks})")
    
    end_time = time.time()
    print(f"   分词完成，用时: {end_time - start_time:.2f}秒")
    print(f"   总分词数: {len(all_words):,}")
    
    if not all_words:
        print("没有找到有效词汇")
        return None
    
    # 5. 统计词频
    print("5. 统计词频...")
    word_counter = Counter(all_words)
    
    # 过滤停用词
    filtered_counter = Counter()
    for word, count in word_counter.items():
        if word not in stop_words and len(word) > 0:
            filtered_counter[word] = count
    
    total_words = sum(filtered_counter.values())
    unique_words = len(filtered_counter)
    
    print(f"   有效词数: {total_words:,}")
    print(f"   唯一词数: {unique_words:,}")
    
    # 6. 获取高频词
    print("6. 获取高频词...")
    top_words = filtered_counter.most_common(top_n)
    
    # 7. 分类统计
    print("7. 分类统计...")
    zhuanhuan_words = []
    emotion_words_list = []
    other_words = []
    
    for word, count in top_words:
        if word in zhuanhuan_keywords:
            zhuanhuan_words.append((word, count))
        elif word in emotion_words:
            emotion_words_list.append((word, count))
        else:
            other_words.append((word, count))
    
    # 8. 显示结果
    print(f"\n分析完成!")
    print(f"前{top_n}个高频词:")
    print("-" * 60)
    
    # 显示摘要
    print(f"\n摘要统计:")
    print(f"  总字符数: {len(text):,}")
    print(f"  有效词数: {total_words:,}")
    print(f"  唯一词数: {unique_words:,}")
    print(f"  角色词数: {len(zhuanhuan_words)}")
    print(f"  情感词数: {len(emotion_words_list)}")
    
    # 显示前20个高频词
    print(f"\n前20个高频词:")
    for i, (word, count) in enumerate(top_words[:20], 1):
        category = ""
        if word in zhuanhuan_keywords:
            category = "[角色]"
        elif word in emotion_words:
            category = "[情感]"
        
        percentage = count / total_words * 100 if total_words > 0 else 0
        print(f"{i:2}. {word:8} : {count:6} ({percentage:.2f}%) {category}")
    
    # 显示角色词
    if zhuanhuan_words:
        print(f"\n《甄嬛传》关键词 (前20个):")
        for i, (word, count) in enumerate(zhuanhuan_words[:20], 1):
            print(f"  {i:2}. {word:8} : {count:6}")
    
    # 显示情感词
    if emotion_words_list:
        print(f"\n情感词汇 (前20个):")
        for i, (word, count) in enumerate(emotion_words_list[:20], 1):
            print(f"  {i:2}. {word:8} : {count:6}")
    
    return {
        'scene_name': scene_name,
        'top_words': top_words,
        'zhuanhuan_words': zhuanhuan_words,
        'emotion_words': emotion_words_list,
        'other_words': other_words,
        'total_words': total_words,
        'unique_words': unique_words,
        'text_length': len(text)
    }

def analyze_from_file(file_path, top_n=100):
    """从文件分析"""
    print(f"从文件读取: {file_path}")
    
    try:
        # 尝试不同编码
        encodings = ['utf-8', 'gbk', 'gb2312', 'utf-8-sig']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"使用编码: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print("无法读取文件，尝试使用二进制模式")
            with open(file_path, 'rb') as f:
                raw_content = f.read()
            # 尝试解码
            for encoding in encodings:
                try:
                    content = raw_content.decode(encoding)
                    break
                except:
                    continue
        
        if content is None:
            print("无法解码文件内容")
            return None
        
        # 获取文件名作为场景名
        scene_name = os.path.splitext(os.path.basename(file_path))[0]
        
        # 分析
        result = analyze_large_text(content, scene_name, top_n)
        
        # 保存结果
        if result:
            save_analysis_result(result)
        
        return result
        
    except Exception as e:
        print(f"读取文件出错: {e}")
        return None

def save_analysis_result(result):
    """保存分析结果"""
    filename = f"高频词分析_{result['scene_name']}.txt"
    
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(f"场景: {result['scene_name']}\n")
        f.write(f"文本长度: {result['text_length']:,} 字符\n")
        f.write(f"有效词数: {result['total_words']:,}\n")
        f.write(f"唯一词数: {result['unique_words']:,}\n")
        f.write("=" * 60 + "\n\n")
        
        # 写入高频词
        f.write(f"前100个高频词:\n")
        f.write("-" * 60 + "\n")
        
        for i, (word, count) in enumerate(result['top_words'], 1):
            category = ""
            if word in zhuanhuan_keywords:
                category = "[角色]"
            elif word in emotion_words:
                category = "[情感]"
            
            percentage = count / result['total_words'] * 100 if result['total_words'] > 0 else 0
            f.write(f"{i:3}. {word:10} : {count:8} ({percentage:.3f}%) {category}\n")
        
        # 写入分类结果
        if result['zhuanhuan_words']:
            f.write(f"\n《甄嬛传》关键词 ({len(result['zhuanhuan_words'])}个):\n")
            for word, count in result['zhuanhuan_words']:
                f.write(f"  {word:10} : {count:8}\n")
        
        if result['emotion_words']:
            f.write(f"\n情感词汇 ({len(result['emotion_words'])}个):\n")
            for word, count in result['emotion_words']:
                f.write(f"  {word:10} : {count:8}\n")
    
    print(f"结果已保存到: {filename}")

def batch_analyze_files(file_patterns=None):
    """批量分析文件"""
    print("批量分析模式")
    print("=" * 60)
    
    # 查找文件
    if file_patterns is None:
        file_patterns = ['*.txt', '*.csv', '*.json']
    
    files = []
    for pattern in file_patterns:
        files.extend([f for f in os.listdir('.') if f.endswith(pattern.replace('*', ''))])
    
    files = list(set(files))  # 去重
    
    if not files:
        print("当前目录下没有找到文本文件")
        return []
    
    print(f"找到 {len(files)} 个文件:")
    for i, f in enumerate(files, 1):
        size = os.path.getsize(f) if os.path.exists(f) else 0
        print(f"  {i:2}. {f} ({size:,} bytes)")
    
    results = []
    for file_path in files:
        print(f"\n{'='*60}")
        print(f"分析文件: {file_path}")
        
        result = analyze_from_file(file_path)
        if result:
            results.append(result)
    
    # 生成汇总报告
    if len(results) > 1:
        generate_batch_summary(results)
    
    return results

def generate_batch_summary(results):
    """生成批量分析汇总报告"""
    summary_file = "批量分析汇总报告.txt"
    
    with open(summary_file, 'w', encoding='utf-8') as f:
        f.write("《甄嬛传》弹幕高频词批量分析汇总报告\n")
        f.write("=" * 80 + "\n\n")
        
        f.write(f"分析文件总数: {len(results)}\n\n")
        
        # 文件摘要
        f.write("各文件分析摘要:\n")
        f.write("-" * 100 + "\n")
        f.write(f"{'文件名':<30} {'字符数':<10} {'词数':<10} {'唯一词':<10} {'角色词':<10} {'情感词':<10} {'高频词1':<15}\n")
        f.write("-" * 100 + "\n")
        
        total_stats = {'chars': 0, 'words': 0, 'unique': 0, 'keywords': 0, 'emotions': 0}
        
        for result in results:
            top_word = result['top_words'][0][0] if result['top_words'] else "无"
            f.write(f"{result['scene_name']:<30} {result['text_length']:<10,} "
                   f"{result['total_words']:<10,} {result['unique_words']:<10,} "
                   f"{len(result['zhuanhuan_words']):<10} {len(result['emotion_words']):<10} "
                   f"{top_word:<15}\n")
            
            total_stats['chars'] += result['text_length']
            total_stats['words'] += result['total_words']
            total_stats['unique'] += result['unique_words']
            total_stats['keywords'] += len(result['zhuanhuan_words'])
            total_stats['emotions'] += len(result['emotion_words'])
        
        f.write("-" * 100 + "\n")
        f.write(f"{'总计':<30} {total_stats['chars']:<10,} {total_stats['words']:<10,} "
               f"{total_stats['unique']:<10,} {total_stats['keywords']:<10} {total_stats['emotions']:<10}\n\n")
        
        # 跨文件高频词
        f.write("跨文件高频词分析:\n")
        f.write("-" * 60 + "\n")
        
        all_word_counter = Counter()
        for result in results:
            for word, count in result['top_words']:
                all_word_counter[word] += count
        
        top_cross_words = all_word_counter.most_common(100)
        
        f.write(f"\n最常出现的100个词汇（跨文件）:\n")
        for i, (word, total_count) in enumerate(top_cross_words, 1):
            category = ""
            if word in zhuanhuan_keywords:
                category = "[角色]"
            elif word in emotion_words:
                category = "[情感]"
            
            f.write(f"{i:3}. {word:12} : {total_count:6} {category}\n")
    
    print(f"\n汇总报告已保存到: {summary_file}")
    
    # 显示关键统计
    print(f"\n批量分析完成!")
    print(f"  分析文件数: {len(results)}")
    print(f"  总字符数: {total_stats['chars']:,}")
    print(f"  总词数: {total_stats['words']:,}")
    print(f"  唯一词数: {total_stats['unique']:,}")

def main():
    """主函数"""
    import time
    
    print("《甄嬛传》大文本高频词分析工具（优化版）")
    print("=" * 60)
    print("特点:")
    print("  1. 高效分词算法，处理大文本")
    print("  2. 分块处理，避免内存溢出")
    print("  3. 批量分析多个文件")
    print("  4. 自动保存结果")
    print("=" * 60)
    
    while True:
        print("\n请选择模式:")
        print("  1. 分析单个大文本文件")
        print("  2. 批量分析多个文件")
        print("  3. 手动输入文本")
        print("  4. 退出")
        
        choice = input("请输入选择 (1/2/3/4): ").strip()
        
        if choice == '1':
            file_path = input("请输入文件路径: ").strip()
            if os.path.exists(file_path):
                analyze_from_file(file_path)
            else:
                print("文件不存在!")
        
        elif choice == '2':
            batch_analyze_files()
        
        elif choice == '3':
            print("请输入文本（输入'END'结束）:")
            lines = []
            while True:
                line = input()
                if line.strip().upper() == 'END':
                    break
                lines.append(line)
            
            text = "\n".join(lines)
            scene_name = input("请输入场景名称: ").strip() or "手动输入"
            analyze_large_text(text, scene_name)
        
        elif choice == '4':
            print("退出程序")
            break
        
        else:
            print("无效选择，请重新输入")

if __name__ == "__main__":
    # 需要导入time模块
    import time
    main()
