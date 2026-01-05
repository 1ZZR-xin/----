import requests
import csv
import time
import random
import re
from datetime import datetime

def fixed_time_danmu_crawler():
    """修复时间显示的弹幕爬虫"""
    
    # 创建会话并设置headers
    session = requests.Session()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.bilibili.com',
        'Origin': 'https://www.bilibili.com'
    }
    session.headers.update(headers)
    
    # 用户输入BV号
    bvid = input("请输入您要爬取的视频BV号: ").strip()
    if not bvid.startswith('BV'):
        print("BV号格式错误，请以'BV'开头。")
        return False
    
    print(f"🎯 开始爬取视频 {bvid} 的弹幕...")
    
    # 获取视频信息
    max_retries = 3
    info_data = None
    
    for attempt in range(max_retries):
        try:
            print(f"尝试获取视频信息... (第 {attempt + 1} 次)")
            info_url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
            
            time.sleep(random.uniform(1, 3))
            
            response = session.get(info_url, timeout=15)
            
            if response.status_code == 200 and response.text.strip():
                info_data = response.json()
                if info_data.get('code') == 0:
                    break
                else:
                    print(f"API返回错误: {info_data.get('message')}")
                    
        except Exception as e:
            print(f"获取视频信息失败: {e}")
    
    if not info_data or info_data.get('code') != 0:
        print("❌ 无法获取视频信息，请检查BV号是否正确")
        return False
    
    # 正常流程
    cid = info_data['data']['cid']
    title = info_data['data']['title']
    owner = info_data['data']['owner']['name']
    print(f"✅ 视频标题: {title}")
    print(f"✅ UP主: {owner}")
    print(f"✅ 视频CID: {cid}")
    
    # 获取弹幕
    danmu_list = get_fixed_time_danmu_data(cid, session)
    
    if danmu_list:
        save_fixed_time_danmu_to_csv(danmu_list, bvid, title, owner)
        return True
    else:
        print("❌ 没有获取到弹幕数据")
        return False

def get_fixed_time_danmu_data(cid, session):
    """获取弹幕数据 - 修复时间显示"""
    try:
        danmu_url = f"https://api.bilibili.com/x/v1/dm/list.so?oid={cid}"
        print(f"获取弹幕URL: {danmu_url}")
        
        response = session.get(danmu_url, timeout=15)
        
        if response.status_code == 200:
            # 直接处理二进制数据，尝试多种编码
            content_bytes = response.content
            encodings = ['gb18030', 'gbk', 'gb2312', 'utf-8', 'latin1']
            xml_content = None
            
            for encoding in encodings:
                try:
                    xml_content = content_bytes.decode(encoding, errors='strict')
                    if '弹幕' in xml_content or '<?xml' in xml_content:
                        print(f"✅ 使用编码 {encoding} 成功")
                        break
                except UnicodeDecodeError:
                    continue
            
            if xml_content is None:
                xml_content = content_bytes.decode('gb18030', errors='ignore')
                print("⚠️ 使用GB18030忽略错误模式")
            
            return parse_fixed_time_danmu_xml(xml_content)
        else:
            print(f"弹幕请求失败: {response.status_code}")
            
    except Exception as e:
        print(f"获取弹幕失败: {e}")
    
    return []

def parse_fixed_time_danmu_xml(xml_content):
    """解析弹幕XML - 修复时间显示问题"""
    if not xml_content:
        return []
    
    danmu_list = []
    pattern = r'<d p="([^"]*)">([^<]*)</d>'
    matches = re.findall(pattern, xml_content)
    
    print(f"找到 {len(matches)} 条弹幕")
    
    # 年份统计和时间戳调试
    year_count = {2023: 0, 2024: 0, 2025: 0}
    timestamp_issues = 0
    
    for i, match in enumerate(matches):
        try:
            params = match[0].split(',')
            raw_content = match[1]
            
            if len(params) >= 8:
                # 解析参数
                appear_time = float(params[0])
                mode = int(params[1])
                font_size = int(params[2])
                color = int(params[3])
                send_timestamp_str = params[4]  # 时间戳字符串
                user_hash = params[6]
                
                # !!! 关键修复：时间戳处理
                send_time = None
                send_year = None
                
                try:
                    # 尝试将时间戳转换为整数
                    send_timestamp = int(float(send_timestamp_str))
                    
                    # 检查时间戳是否合理（在2000-2030年之间）
                    if send_timestamp > 946684800 and send_timestamp < 1900000000:
                        send_time = datetime.fromtimestamp(send_timestamp)
                        send_year = send_time.year
                    else:
                        # 时间戳不合理，使用当前时间作为备选
                        timestamp_issues += 1
                        send_time = datetime.now()
                        send_year = send_time.year
                        print(f"⚠️ 第{i+1}条弹幕时间戳异常: {send_timestamp_str}")
                        
                except (ValueError, TypeError, OSError) as e:
                    # 时间戳解析失败，使用当前时间
                    timestamp_issues += 1
                    send_time = datetime.now()
                    send_year = send_time.year
                    print(f"⚠️ 第{i+1}条弹幕时间戳解析失败: {send_timestamp_str}, 错误: {e}")
                
                # 筛选2023-2025年的数据
                if send_year not in [2023, 2024, 2025]:
                    continue
                
                # 统计符合条件的数据
                year_count[send_year] = year_count.get(send_year, 0) + 1
                
                # 修复内容编码
                content = fix_content_encoding(raw_content)
                
                # 格式化时间位置
                minutes = int(appear_time // 60)
                seconds = int(appear_time % 60)
                time_pos = f"{minutes}:{seconds:02d}"
                
                # 颜色处理 - 转换为中文
                color_hex = f"#{color:06X}"
                color_chinese = color_to_chinese(color_hex)
                
                # 弹幕模式描述
                mode_desc = "滚动弹幕" if mode == 1 else "顶部弹幕" if mode == 5 else "底部弹幕" if mode == 4 else f"模式{mode}"
                
                # 字体大小描述
                font_desc = "正常" if font_size == 25 else "较大" if font_size > 25 else "较小"
                
                danmu_data = {
                    '发送日期': send_time.strftime('%Y-%m-%d') if send_time else '时间未知',
                    '发送时间': send_time.strftime('%H:%M:%S') if send_time else '时间未知',
                    '发送年份': send_year if send_year else '未知',
                    '时间位置': time_pos,
                    '出现时间秒': round(appear_time, 2),
                    '弹幕内容': content,
                    '用户ID': user_hash[:8] + '...',
                    '弹幕颜色': color_chinese,
                    '颜色代码': color_hex,
                    '弹幕模式': mode_desc,
                    '字体大小': font_desc,
                    '弹幕长度': len(content),
                    '原始时间戳': send_timestamp_str  # 用于调试
                }
                
                danmu_list.append(danmu_data)
                
                # 显示前几条的时间信息用于调试
                if i < 3:
                    print(f"  示例 {i+1}: 时间戳={send_timestamp_str}, 日期={danmu_data['发送日期']}")
                    
        except Exception as e:
            print(f"❌ 解析第{i+1}条弹幕失败: {e}")
            continue
    
    # 打印年份统计和时间戳问题
    print(f"\n📅 符合条件的弹幕年份分布:")
    for year in [2023, 2024, 2025]:
        count = year_count.get(year, 0)
        print(f"   {year}年: {count}条")
    
    if timestamp_issues > 0:
        print(f"⚠️ 时间戳问题: {timestamp_issues} 条弹幕的时间戳异常")
    
    return danmu_list

def fix_content_encoding(content):
    """修复内容编码"""
    if not content:
        return content
    
    # 如果是乱码模式（包含特殊字符），尝试修复
    if 'å' in content or 'ä' in content or 'è' in content or 'é' in content:
        try:
            # 可能是UTF-8被错误解码为latin1
            if isinstance(content, str):
                # 重新编码为latin1再解码为UTF-8
                content_bytes = content.encode('latin1')
                content = content_bytes.decode('utf-8')
        except:
            pass
    
    return content

def color_to_chinese(color_hex):
    """将十六进制颜色转换为中文颜色名称"""
    color_map = {
        '#FFFFFF': '白色',
        '#000000': '黑色',
        '#FF0000': '红色',
        '#FF5E5E': '浅红色',
        '#E70012': '深红色',
        '#FFAEC9': '粉红色',
        '#FF7F27': '橙色',
        '#FFC90E': '黄色',
        '#FEF102': '亮黄色',
        '#22B14C': '绿色',
        '#90C320': '浅绿色',
        '#00A2E8': '蓝色',
        '#3F48CC': '深蓝色',
        '#1D9AA5': '青色',
        '#A349A4': '紫色',
        '#B97A57': '棕色',
        '#7F7F7F': '灰色',
        '#C3C3C3': '浅灰色'
    }
    
    color_hex_upper = color_hex.upper()
    return color_map.get(color_hex_upper, '其他颜色')

def save_fixed_time_danmu_to_csv(danmu_list, bvid, title, owner):
    """保存弹幕到CSV - 移除调试字段"""
    if not danmu_list:
        return
    
    filename = f"弹幕数据_{bvid}_{len(danmu_list)}条.csv"
    
    try:
        # 字段列表 - 移除原始时间戳字段
        save_fields = [
            '发送日期', '发送时间', '发送年份', '时间位置', 
            '出现时间秒', '弹幕内容', '用户ID', '弹幕颜色', 
            '颜色代码', '弹幕模式', '字体大小', '弹幕长度'
        ]
        
        # 创建最终数据（移除调试字段）
        final_data = []
        for danmu in danmu_list:
            final_danmu = {field: danmu[field] for field in save_fields}
            final_data.append(final_danmu)
        
        with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
            writer = csv.DictWriter(f, fieldnames=save_fields)
            writer.writeheader()
            writer.writerows(final_data)
        
        print(f"✅ 成功保存 {len(danmu_list)} 条弹幕到 {filename}")
        
        # 显示统计信息
        show_fixed_time_statistics(danmu_list, title, owner)
        
        # 显示弹幕预览
        show_fixed_time_preview(danmu_list)
            
    except Exception as e:
        print(f"保存文件失败: {e}")

def show_fixed_time_statistics(danmu_list, title, owner):
    """显示统计信息"""
    print(f"\n📊 统计信息:")
    print(f"   视频标题: {title}")
    print(f"   UP主: {owner}")
    print(f"   总弹幕数: {len(danmu_list)} 条")
    
    # 检查时间未知的弹幕
    unknown_time_count = sum(1 for danmu in danmu_list if danmu['发送日期'] == '时间未知')
    if unknown_time_count > 0:
        print(f"⚠️  时间未知的弹幕: {unknown_time_count} 条")
    
    # 年份统计
    year_stats = {}
    for danmu in danmu_list:
        year = danmu['发送年份']
        if year != '未知':
            year_stats[year] = year_stats.get(year, 0) + 1
    
    print(f"\n📅 最终年份分布:")
    for year in sorted(year_stats.keys()):
        print(f"   {year}年: {year_stats[year]}条")

def show_fixed_time_preview(danmu_list):
    """显示弹幕预览"""
    print(f"\n📝 弹幕预览 (前10条):")
    print("=" * 70)
    
    for i, danmu in enumerate(danmu_list[:10], 1):
        content = danmu['弹幕内容']
        print(f"{i}. [{danmu['发送日期']} {danmu['发送时间']}]")
        print(f"   用户: {danmu['用户ID']} | 颜色: {danmu['弹幕颜色']}")
        print(f"   内容: {content}")
        print()

def main():
    print("🎬 B站弹幕爬虫 (时间修复版)")
    print("=" * 50)
    print("💡 此版本专门修复时间显示问题：")
    print("   • 增强时间戳解析")
    print("   • 处理异常时间戳")
    print("   • 显示时间戳问题统计")
    print("=" * 50)
    
    # 开始爬取
    success = fixed_time_danmu_crawler()
    
    if not success:
        print("\n❌ 爬取失败，请检查网络连接或BV号是否正确")

if __name__ == "__main__":
    main()
