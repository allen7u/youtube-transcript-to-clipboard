import json
from youtube_transcript_api import YouTubeTranscriptApi
import sys
import re
import requests
import pyperclip
from copy2clip import clip_files

# 从命令行参数读取URL
try:
    url = sys.argv[1]
    if url == "":
        raise IndexError
except IndexError:
    clipboard_content = pyperclip.paste()
    print(clipboard_content)
    # 从剪贴板内容中提取YouTube URL
    urls = [line.strip() for line in clipboard_content.splitlines() if '/watch?v=' in line]
else:
    urls = [url]

print(urls)

for url in urls:

    print('正在处理:', url)

    video_id = re.search(r'v=([^&]+)', url).group(1)
    print(video_id)
    # 重构完整的YouTube URL
    url = 'https://www.youtube.com/watch?v=' + video_id
    print(url)

    response = requests.get(url)

    title = ''
    if response.status_code == 200:
        html = response.text
        try:
            title = html.split('<title>')[1].split('</title>')[0]
            print(title)
        except IndexError:
            title = url.split('?search_query=')[-1][:20]
            if title:
                print(title)
            else:
                print("无法找到视频标题。")
    else:
        print("获取视频标题时未得到200响应。")

    # 创建以视频标题为文件名的文件，首先转义标题
    escaped_title = re.sub(r'[<>:"/\\|?*]', '', title)

    try:
        # 获取字幕
        captions = YouTubeTranscriptApi.get_transcript(video_id)

        import os
        
        # 确保目录存在
        os.makedirs('Raw-Timestamp-JSON', exist_ok=True)
        
        with open(f'Raw-Timestamp-JSON/{escaped_title}.txt', 'w', encoding='utf-8') as file:
            json.dump(captions, file, indent=4, ensure_ascii=False)

        def format_time(seconds):
            hours = int(seconds) // 3600
            minutes = (int(seconds) % 3600) // 60
            seconds = int(seconds) % 60
            return f"{hours}:{minutes:02}:{seconds:02}"

        with open(f'{escaped_title}.txt', 'w', encoding='utf-8') as file:
            # 将字幕写入文件
            file.write('ASR 转录:\n\n')
            captions_list = 'ASR 转录:\n\n'

            last_start = 0
            for i, caption in enumerate(captions):
                if i == 0:
                    file.write(f"{format_time(caption['start'])}\n {caption['text']}\n")
                    captions_list += f"{format_time(caption['start'])}:\n {caption['text']}\n"
                elif caption['start'] - last_start > 10:
                    file.write(f"{format_time(caption['start'])}\n {caption['text']}\n")
                    captions_list += f"{format_time(caption['start'])}:\n {caption['text']}\n"
                    last_start = caption['start']
                else:
                    file.write(f"{caption['text']}\n")
                    captions_list += f"{caption['text']}\n"
            
            # pyperclip.copy(captions_list)
            
        # 获取文件的绝对路径
        file_path = os.path.abspath(f'{escaped_title}.txt')
        
        # 将文件路径复制到剪贴板
        clip_files([file_path])
        
        print(f'字幕已保存到 {title}.txt 并复制该 txt 文件到剪贴板。\n')

    except Exception as e:
        print(e)
        print(f'处理任务 {escaped_title} 失败....txt')
        with open(f'- 失败任务 {escaped_title}....txt', 'w', encoding='utf-8') as file:
            file.write('')
    
    print(f'{escaped_title} 处理完成')

