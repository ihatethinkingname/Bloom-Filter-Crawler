import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
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

        # <a href="...">
        for link in soup.find_all('a', href=True):
            full_url = urljoin(page_url, link['href'])
            parsed = urlparse(full_url)
            if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
                new_urls.append(full_url)

        # # <img src="...">
        # for img in soup.find_all('img', src=True):
        #     full_url = urljoin(page_url, img['src'])
        #     parsed = urlparse(full_url)
        #     if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
        #         new_urls.append(full_url)

        # # <script src="...">
        # for script in soup.find_all('script', src=True):
        #     full_url = urljoin(page_url, script['src'])
        #     parsed = urlparse(full_url)
        #     if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
        #         new_urls.append(full_url)

        # # <link rel="stylesheet" href="...">
        # for link in soup.find_all('link', href=True):
        #     if link.get('rel') and 'stylesheet' in link.get('rel'):
        #         full_url = urljoin(page_url, link['href'])
        #         parsed = urlparse(full_url)
        #         if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
        #             new_urls.append(full_url)

        # # <form action="...">
        # for form in soup.find_all('form', action=True):
        #     full_url = urljoin(page_url, form['action'])
        #     parsed = urlparse(full_url)
        #     if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
        #         new_urls.append(full_url)

        # # <iframe src="...">
        # for iframe in soup.find_all('iframe', src=True):
        #     full_url = urljoin(page_url, iframe['src'])
        #     parsed = urlparse(full_url)
        #     if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
        #         new_urls.append(full_url)

        title = soup.title.string.strip() if soup.title else ''
        return new_urls, title

# class Parser:
#     def parse(self, page_url, html_content):
#         soup = BeautifulSoup(html_content, 'html.parser')  # 使用快速解析器
#         new_urls = deque()
#         for link in soup.find_all('a', href=True):
#             full_url = urljoin(page_url, link['href'])
#             if full_url.startswith('https://quotes.toscrape.com/'):
#                 new_urls.append(full_url)
#         return new_urls, soup.title.string if soup.title else ''

# class Parser:
#     def __init__(self, allowed_domain):
#         self.allowed_domain = allowed_domain

#     def parse(self, page_url, html_content):
#         soup = BeautifulSoup(html_content, 'html.parser')
#         new_urls = deque()

#         # <a href="...">
#         for link in soup.find_all('a', href=True):
#             full_url = urljoin(page_url, link['href'])
#             parsed = urlparse(full_url)
#             if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                 new_urls.append(full_url)
        
#         # <img src="...">
#         for img in soup.find_all('img', src=True):
#             full_url = urljoin(page_url, img['src'])
#             parsed = urlparse(full_url)
#             if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                 new_urls.append(full_url)

#         # <script src="...">
#         for script in soup.find_all('script', src=True):
#             full_url = urljoin(page_url, script['src'])
#             parsed = urlparse(full_url)
#             if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                 new_urls.append(full_url)

#         # <link rel="stylesheet" href="...">
#         for link in soup.find_all('link', href=True):
#             if link.get('rel') and 'stylesheet' in link.get('rel'):
#                 full_url = urljoin(page_url, link['href'])
#                 parsed = urlparse(full_url)
#                 if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                     new_urls.append(full_url)

#         # <form action="...">
#         for form in soup.find_all('form', action=True):
#             full_url = urljoin(page_url, form['action'])
#             parsed = urlparse(full_url)
#             if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                 new_urls.append(full_url)

#         # <iframe src="...">
#         for iframe in soup.find_all('iframe', src=True):
#             full_url = urljoin(page_url, iframe['src'])
#             parsed = urlparse(full_url)
#             if parsed.scheme in ('http', 'https') and parsed.netloc == self.allowed_domain:
#                 new_urls.append(full_url)

#         title = soup.title.string.strip() if soup.title else ''
#         print("parsed.netloc:", parsed.netloc, "allowed:", self.allowed_domain)
#         return new_urls, title
