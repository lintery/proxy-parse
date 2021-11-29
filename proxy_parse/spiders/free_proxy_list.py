from scrapy import Spider

from proxy_parse.models import Proxy


class FreeProxyListSpider(Spider):
    name = "free-proxy-list"
    start_urls = ["https://free-proxy-list.net/"]

    def parse(self, response, **kwargs):
        proxies_tags = response.xpath(
            '//table[@class="table table-striped table-bordered"]'
        )[0]
        proxies_ip = proxies_tags.xpath("//tr//td[1]//text()")[:-16]
        proxies_port = proxies_tags.xpath("//tr//td[2]//text()")
        proxies_protocol = proxies_tags.xpath("//tr//td[7]//text()")

        for i, ip in enumerate(proxies_ip):
            protocol = "https://" if proxies_protocol[i].get() == "yes" else "http://"
            yield Proxy(proxy=protocol + ip.get() + ":" + proxies_port[i].get())
