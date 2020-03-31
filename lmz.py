'''
@Author: your name
@Date: 2020-03-24 23:19:31
@LastEditTime: 2020-03-31 16:04:50
@LastEditors: Please set LastEditors
@Description: In User Settings Edit
@FilePath: /code/effectivepython.py
'''

# 将ts合并成mp4
# # 主要是需要moviepy这个库
# from moviepy.editor import *
# import os
# from natsort import natsorted
# # 定义一个数组
# L = []
# # 访问 video 文件夹 (假设视频都放在这里面)
# for root, dirs, files in os.walk("/Users/xujun/Downloads"):
#     # 按文件名排序
#     files = natsorted(files)
#     # 遍历所有文件
#     for file in files:
#         # 如果后缀名为 .ts
#         if os.path.splitext(file)[1] == '.ts':
#             # 拼接成完整路径
#             filePath = os.path.join(root, file)
#             # 载入视频
#             video = VideoFileClip(filePath)
#             # 添加到数组
#             L.append(video)

# # 拼接视频
# final_clip = concatenate_videoclips(L)

# # 生成目标视频文件
# final_clip.to_videofile("/Users/xujun/Downloads/合成后的视频.mp4", fps=24, remove_temp=False)


import os
import requests
import re
import json
from bs4 import BeautifulSoup as bs
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import threading

headers ={
    "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36"
    }

path = 'lmz'
if not os.path.exists(path):
    os.mkdir(path)

def downloader(url,filename):
    url = "https://www.meijui.com/"+url   
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    resp = requests.get(url,verify=False)
    player_data = re.findall('player_data=(\{.*?\})',resp.text)
    player_data = json.loads(player_data[0])
    
    m3u8 = player_data['url']
    m3u8 = m3u8.replace('index.m3u8','800k/hls/index.m3u8')
    ts_res = requests.get(m3u8)
    ts = ts_res.text.split('\n')
    ts_list = []
    filepath = path+'/'+filename
    if not os.path.exists(filepath):
        os.mkdir(filepath)
    for t in ts:
        if 'ts' in t:
            ts_url = m3u8.replace('index.m3u8',t)
            content = requests.get(ts_url)
            print('downloading:{}'.format(t))
            with open(filepath+'/'+t,'wb') as f:
                f.write(content.content)
            print('downloading ok')

def run():
    url = "https://www.meijui.com/video/82536-1-6.html"
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    resp = requests.get(url,headers=headers,verify=False)
    soup = bs(resp.text,'lxml')
    ul = soup.find(class_='stui-content__playlist clearfix')
    print(ul)
    a = ul.find_all('a')
    li_dict = {}
    threadlist = []
    for l in a:
        t = threading.Thread(target=downloader,args=(l.get('href'),l.text))
        threadlist.append(t)
        print('starting download {}'.format(l.text))
    for x in threadlist:
        x.start()
    for x in threadlist:
        x.join()


if __name__ == "__main__":
    run()
