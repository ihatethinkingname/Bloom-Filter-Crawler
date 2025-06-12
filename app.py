from flask import Flask, jsonify, render_template, request
from stats_share import crawler_stats, start_crawler
import threading
import sys
from pybloom_live import BloomFilter
import math

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def calculate_memory_usage(capacity, urls_set_size=None):
    # 获取实际使用的错误率
    error_rate = crawler_stats.get('error_rate', 0.1)
    
    # 计算布隆过滤器参数
    m = int(math.ceil(-(capacity * math.log(error_rate)) / (math.log(2) * math.log(2))))  # 位数组大小,向上取整
    k = int(round(-math.log(error_rate) / math.log(2)))  # 哈希函数个数,四舍五入
    
    # 使用实际参数创建布隆过滤器
    bloom = BloomFilter(capacity=capacity, error_rate=error_rate)
    bloom_memory = sys.getsizeof(bloom)
    
    # 使用实际的URL集合
    urls_set = crawler_stats.get('visited_urls', set())
    set_memory = sys.getsizeof(urls_set)
    
    return {
        'bloom_memory': bloom_memory,
        'set_memory': set_memory,
        'hash_functions': k,
        'bit_array_size': m
    }

def format_size(size_in_bytes):
    """格式化字节大小为人类可读格式"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

@app.route('/stats')
def stats():
    stats_data = crawler_stats.copy()
    
    # 如果爬虫已完成,添加内存使用信息
    if stats_data.get('is_finished', False):
        memory_stats = calculate_memory_usage(
            capacity=stats_data.get('total_checked', 0),
            urls_set_size=len(stats_data.get('visited_urls', set()))
        )
        stats_data.update({
            'bloom_filter_memory': f"{memory_stats['bloom_memory']} bytes",
            'set_memory': f"{memory_stats['set_memory']} bytes",
            'hash_functions': memory_stats['hash_functions'],
            'bit_array_size': memory_stats['bit_array_size']
        })
    
    return jsonify(stats_data)

@app.route('/start_crawler', methods=['POST'])
def start_new_crawler():
    params = request.json
    capacity = int(params.get('capacity', 220))
    error_rate = float(params.get('error_rate', 0.1))
    
    # 重置统计数据
    crawler_stats.clear()
    crawler_stats.update({
        "total_checked": 0,
        "duplicate_count": 0,
        "false_positive_count": 0,
        "dedup_rate": 0.0,
        "false_positive_rate": 0.0,
        "is_finished": False,
        "capacity": capacity,      # 保存实际使用的容量
        "error_rate": error_rate   # 保存实际使用的错误率
    })
    
    # 启动新的爬虫线程
    threading.Thread(
        target=start_crawler,
        args=(capacity, error_rate),
        daemon=True
    ).start()
    
    return jsonify({"status": "started"})

if __name__ == '__main__':
    app.run(debug=False, port=5000)
