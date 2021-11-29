from scrapy import Spider

from proxy_parse.models import Proxy


class ProxySearcherSpider(Spider):
    name = "proxy-searcher"
    start_urls = [
        "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=http&filtered=true",
        "http://proxysearcher.sourceforge.net/Proxy%20List.php?type=socks&filtered=true",
    ]

    def parse(self, response, **kwargs):
        proxies_tags = response.xpath('//div[@class="right-panel-advertising"]//text()')
        protocol = "socks://" if "socks" in response.url else "http://"
        for i, tag in enumerate(proxies_tags[3:-2]):
            yield Proxy(proxy=protocol + tag.get())
