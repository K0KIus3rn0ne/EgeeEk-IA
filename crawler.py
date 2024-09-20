import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests

class WebCrawler(scrapy.Spider):
    name = "web_crawler"

    def __init__(self, search_query, *args, **kwargs):
        super(WebCrawler, self).__init__(*args, **kwargs)
        self.search_query = search_query.replace(" ", "+")
        self.start_urls = [f'https://www.google.com/search?q={self.search_query}']

    def parse(self, response):
        soup = BeautifulSoup(response.text, 'html.parser')
        results = []

        # Filtrando para capturar apenas resultados mais relevantes (títulos)
        for result in soup.select('h3'):
            title = result.get_text()
            if title and "Wikipedia" in title or "relevante" in title:
                results.append(title)

        return results

# Função para iniciar o crawler
def search_web(query):
    process = CrawlerProcess(settings={
        "LOG_LEVEL": "ERROR",
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36",
    })

    crawler = WebCrawler(search_query=query)
    process.crawl(crawler)
    process.start()

    return crawler.crawled_results  # Retorna os resultados encontrados