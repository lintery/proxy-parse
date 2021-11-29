from scrapy import Spider

from proxy_parse.models import Proxy


class BlogSpotSpider(Spider):
    name = "blog-spot"
    start_urls = ["https://getfreeproxylists.blogspot.com/"]

    def parse(self, response, **kwargs):
        proxies_list = response.xpath(
            '//div[@class="date-posts"]/div[1]/div[1]/div[2]/text()'
        )[:-2]
        http_num = int(proxies_list[0].get().split(": ")[1].split()[0])
        https_num = int(proxies_list[0].get().split(", ")[1].split()[0])

        for i, proxy in enumerate(proxies_list[1:]):
            if ":" not in proxy.get():
                continue
            if i + 1 <= http_num:
                protocol = "http://"
            elif http_num < i + 1 <= https_num:
                protocol = "https://"
            else:
                protocol = "socks://"

            yield Proxy(proxy=protocol + proxy.get())
