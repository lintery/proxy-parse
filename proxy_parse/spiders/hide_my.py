from scrapy import Spider

from proxy_parse.models import Proxy


class HideMySpider(Spider):
    name = "hyde_my"
    start_urls = ["https://hidemy.name/ru/proxy-list/"]

    def parse(self, response, **kwargs):
        proxies_table = response.xpath("//tbody//tr")

        for proxies_tag in proxies_table:
            if proxies_tag.xpath("td[5]/text()").get == "HTTP":
                protocol = "http://"
            elif proxies_tag.xpath("td[5]/text()").get == "HTTP,HTTPS":
                protocol = "https://"
            else:
                protocol = "socks://"

            proxy_ip = proxies_tag.xpath("td[1]/text()").get()
            proxy_port = proxies_tag.xpath("td[2]/text()").get()
            yield Proxy(proxy=protocol + proxy_ip + ":" + proxy_port)

        if "?start=" not in response.url:
            current_page = 0
        else:
            current_page = int(response.url.split("=")[1])

        last_page = response.xpath('//div[@class="pagination"]/ul')[0]
        if last_page.xpath("li[last()]/@class").get() == "next_array":
            last_page = last_page.xpath("li[last()-1]/a/text()").get()
        else:
            last_page = last_page.xpath("/li[last()]/a/text()").get()

        if not last_page or (int(last_page) + 1) * 64 <= current_page:
            return

        yield response.follow(
            f"https://hidemy.name/ru/proxy-list/?start={current_page + 64}",
            callback=self.parse,
        )
