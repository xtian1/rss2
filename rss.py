import requests
from feedgen.feed import FeedGenerator
import time

# B站UP主UID
UID = '7788379'
# B站API接口（获取投稿视频）
API_URL = f'https://api.bilibili.com/x/space/arc/search?mid={UID}&ps=10&tid=0&pn=1&order=pubdate&jsonp=jsonp'

def fetch_bilibili_videos():
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }
    resp = requests.get(API_URL, headers=headers)

    print("状态码：", resp.status_code)
    print("返回内容：", resp.text[:200])  # 只打印前200字符

    if resp.status_code != 200:
        print("请求失败，状态码：", resp.status_code)
        print(resp.text)
        exit()

    try:
        data = resp.json()
        print("JSON解析成功")
        videos = data['data']['list']['vlist']
        return videos
    except Exception as e:
        print("JSON解析失败：", e)

def generate_rss(videos, output_file='bilibili_rss.xml'):
    fg = FeedGenerator()
    fg.title('B站UP主最新投稿')
    fg.link(href=f'https://space.bilibili.com/{UID}', rel='alternate')
    fg.description('自动抓取B站UP主最新投稿')
    fg.language('zh-cn')

    for v in videos:
        fe = fg.add_entry()
        fe.title(v['title'])
        fe.link(href=f"https://www.bilibili.com/video/{v['bvid']}")
        fe.description(v['description'] or v['title'])
        fe.pubDate(time.strftime('%a, %d %b %Y %H:%M:%S +0800', time.localtime(v['created'])))

    fg.rss_file(output_file)
    print(f"RSS已生成：{output_file}")

if __name__ == '__main__':
    videos = fetch_bilibili_videos()
    if videos:
        generate_rss(videos)
    else:
        print("未获取到视频数据，无法生成RSS。")