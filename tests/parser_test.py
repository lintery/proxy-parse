from proxy_parse import ProxyParser
from proxy_parse.spiders import HideMySpider


def test_proxy_parser():
    proxy_parser = ProxyParser(scrapy_spiders=[HideMySpider])
    result = proxy_parser.parse()
    assert type(result) is list
    assert all(type(proxy) is str and ":" in proxy for proxy in result)
