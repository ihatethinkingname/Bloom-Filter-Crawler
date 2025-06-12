from pybloom_live import BloomFilter
from web_part import Downloader,Parser
from data_part import DataSaver
from concurrent.futures import ThreadPoolExecutor, as_completed
from collections import deque
from stats_share import crawler_stats
import threading

from app import app  # 假设app.py里有app=Flask(__name__)

def run_flask():
    app.run(port=5000, debug=False, use_reloader=False)

if __name__ == "__main__":
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()

start_url = "https://quotes.toscrape.com/"
visited_bloom = BloomFilter(capacity=220, error_rate=0.1)
visited_set = set()
url_queue = deque([start_url])
# MAX_PAGES = 1000
MAX_PAGES = None

total_checked = 0
duplicate_count = 0
false_positive_count = 0

downloader = Downloader()
parser = Parser('quotes.toscrape.com')
# parser = Parser()
saver = DataSaver()

def print_crawl_progress(i, total, url):
    print(f"[{i}/{total}] 正在抓取页面: {url}")

def print_stats(stage, total_checked, duplicate_count, false_positive_count):
    dedup_rate = duplicate_count / total_checked if total_checked else 0
    false_positive_rate = (false_positive_count / (total_checked - duplicate_count + false_positive_count)) if duplicate_count else 0

    # 更新共享数据
    crawler_stats["total_checked"] = total_checked
    crawler_stats["duplicate_count"] = duplicate_count
    crawler_stats["false_positive_count"] = false_positive_count
    crawler_stats["dedup_rate"] = dedup_rate
    crawler_stats["false_positive_rate"] = false_positive_rate

    print(f"\n📊 [{stage}] 统计报告")
    print("-" * 40)
    print(f"总抓取 URL 数    : {total_checked}")
    print(f"识别为重复的数目 : {duplicate_count}")
    print(f"误判为重复的数目 : {false_positive_count}")
    print(f"✔ 去重率         : {dedup_rate:.2%}")
    print(f"⚠ 误判率         : {false_positive_rate:.2%}")
    print("-" * 40)


def crawl_one(url):
    global total_checked, duplicate_count, false_positive_count
    result = {'new_urls': [], 'title': '', 'url': url}

    if url in visited_bloom:
        duplicate_count += 1
        if url not in visited_set:
            false_positive_count += 1
        return result

    html = downloader.download(url)
    if html:
        visited_bloom.add(url)
        visited_set.add(url)
        new_urls, title = parser.parse(url, html)
        saver.save(url, title)
        result['new_urls'] = new_urls
        result['title'] = title
    return result

next_print = 50  # 下一次统计输出的阈值

with ThreadPoolExecutor(max_workers=10) as executor:
    # while url_queue and total_checked < MAX_PAGES:
    while url_queue and (MAX_PAGES is None or total_checked < MAX_PAGES):
        current_batch = []
        while url_queue and len(current_batch) < 10:
            current_batch.append(url_queue.popleft())

        futures = [executor.submit(crawl_one, url) for url in current_batch]
        for future in as_completed(futures):
            total_checked += 1
            result = future.result()
            # print_crawl_progress(total_checked, MAX_PAGES, result['url'])
            url_queue.extend(result['new_urls'])

            # 每隔一定数量输出一次统计信息
            if total_checked >= next_print:
                print_stats(f"第 {total_checked} 次检查", total_checked, duplicate_count, false_positive_count)
                next_print += 50

print_stats("最终统计", total_checked-1, duplicate_count, false_positive_count)

saver.close()