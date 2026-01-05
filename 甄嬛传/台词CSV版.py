from docx import Document
import pandas as pd
import re

# 1. 读取 Word 文档（一定要带 .docx）
doc = Document("甄嬛传台词.docx")

rows = []

# 2. 只匹配「人物名:台词内容」
dialogue_pattern = re.compile(r'^([\u4e00-\u9fa5]{1,4})[:：](.+)$')

for para in doc.paragraphs:
    text = para.text.strip()
    if not text:
        continue

    # 3. 跳过场景说明，如 (碎玉轩,众人剪窗花)
    if text.startswith("(") or text.startswith("（"):
        continue

    # 4. 匹配台词
    match = dialogue_pattern.match(text)
    if match:
        speaker = match.group(1).strip()
        dialogue = match.group(2).strip()

        rows.append({
            "speaker": speaker,
            "dialogue": dialogue
        })

# 5. 转成 CSV
df = pd.DataFrame(rows)
df.to_csv("test_dialogue.csv", index=False, encoding="utf-8-sig")

print(f"✅ 成功提取台词 {len(df)} 条，已生成 test_dialogue.csv")
