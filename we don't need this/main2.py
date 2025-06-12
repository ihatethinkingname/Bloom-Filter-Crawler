from pybloom_live import BloomFilter
from collections import deque
from web_part import Downloader,Parser
from data_part import DataSaver

START_URL = 'https://quotes.toscrape.com/'
MAX_PAGES = 500

visited_bloom = BloomFilter(capacity=1000, error_rate=0.1)
visited_set = set()
url_queue = deque([START_URL])
total_checked = 0
duplicate_count = 0
false_positive_count = 0

downloader = Downloader()
parser = Parser()
saver = DataSaver()

while url_queue and total_checked < MAX_PAGES:
    current_url = url_queue.popleft()
    total_checked += 1

    if current_url in visited_bloom:
        duplicate_count += 1
        if current_url not in visited_set:
            false_positive_count += 1
        continue

    html = downloader.download(current_url)
    if html is None:
        print(f'抓取失败: {current_url}')
        continue

    visited_bloom.add(current_url)
    visited_set.add(current_url)
    print(f'正在抓取: {current_url}')

    new_urls, title = parser.parse(current_url, html)
    saver.save(current_url, title)

    url_queue.extend(new_urls)

    if total_checked % 50 == 0:
        dedup_rate = duplicate_count / total_checked
        false_positive_rate = (false_positive_count / duplicate_count) if duplicate_count else 0
        print(f'\n--- 第 {total_checked} 次检查 ---')
        print(f'已检查总数: {total_checked}')
        print(f'重复URL数: {duplicate_count}')
        print(f'误判重复数: {false_positive_count}')
        print(f'去重率: {dedup_rate:.4f}')
        print(f'估算误判率: {false_positive_rate:.4f}\n')

saver.close()
print("爬取结束。")
