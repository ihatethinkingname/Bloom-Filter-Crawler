from pybloom_live import BloomFilter
from web_part import Downloader, Parser
from data_part import DataSaver
from collections import deque
from concurrent.futures import ThreadPoolExecutor, as_completed

# 共享的统计数据
crawler_stats = {
    "total_checked": 0,
    "duplicate_count": 0,
    "false_positive_count": 0,
    "dedup_rate": 0.0,
    "false_positive_rate": 0.0,
    "is_finished": False
}

def start_crawler(capacity, error_rate):
    """爬虫主函数"""
    start_url = "https://quotes.toscrape.com/"
    visited_bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
    visited_set = set()
    url_queue = deque([start_url])
    
    downloader = Downloader()
    parser = Parser('quotes.toscrape.com')
    saver = DataSaver()
    
    def crawl_one(url):
        result = {'new_urls': [], 'title': '', 'url': url}
        
        if url in visited_bloom:
            if url not in visited_set:
                crawler_stats["false_positive_count"] += 1
            crawler_stats["duplicate_count"] += 1
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
    
    with ThreadPoolExecutor(max_workers=10) as executor:
        while url_queue:
            current_batch = []
            while url_queue and len(current_batch) < 10:
                current_batch.append(url_queue.popleft())
                
            futures = [executor.submit(crawl_one, url) for url in current_batch]
            for future in as_completed(futures):
                crawler_stats["total_checked"] += 1
                result = future.result()
                url_queue.extend(result['new_urls'])
                
                # 更新统计数据
                if crawler_stats["total_checked"] > 0:
                    crawler_stats["dedup_rate"] = crawler_stats["duplicate_count"] / crawler_stats["total_checked"]
                    if crawler_stats["duplicate_count"] > 0:
                        crawler_stats["false_positive_rate"] = (
                            crawler_stats["false_positive_count"] /
                            (crawler_stats["total_checked"] - crawler_stats["duplicate_count"] + crawler_stats["false_positive_count"])
                        )
    
    # saver.close()
    crawler_stats["is_finished"] = True