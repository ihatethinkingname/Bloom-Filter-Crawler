import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin,urlparse
from collections import deque

class Downloader:
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/90 Safari/537.36'
        }

    def download(self, url):
        try:
            response = self.session.get(url, headers=self.headers, timeout=5)
            if response.status_code == 200:
                return response.text
        except requests.RequestException:
            return None

class Parser:
    def __init__(self, allowed_domain):
        self.allowed_domain = allowed_domain

    def parse(self, page_url, html_content):
        soup = BeautifulSoup(html_content, 'html.parser')
        new_urls = deque()
        for link in soup.find_all('a', href=True):
            full_url = urljoin(page_url, link['href'])
            parsed = urlparse(full_url)
            if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
                new_urls.append(full_url)
        return new_urls, soup.title.string if soup.title else ''

