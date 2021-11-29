from typing import Optional, List, Type

from scrapy import signals, Spider
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from proxy_parse.proxy.abc import ABCProxyParser
from proxy_parse.spiders import (
    FreeProxyListSpider,
    BlogSpotSpider,
    ProxySearcherSpider,
    HideMySpider,
)


class ProxyParser(ABCProxyParser):
    proxies: List[str] = []

    def __init__(
        self,
        path_to_file: Optional[str] = None,
        proxy_limit: int = 0,
        scrapy_spiders: Optional[List[Type[Spider]]] = None,
        scrapy_settings: Optional[dict] = None,
    ):
        """
        :param path_to_file: Path to file to save proxies,
        if not specified, the proxies will not be saved to the file
        :param proxy_limit: Limit of returned proxies from the "parse" method,
        if 0, no limit
        :param scrapy_settings: Allows you to set custom settings for scrapy.CrawlerProcess
        :param scrapy_spiders: You can add your own spiders. Examples can be found
        in the "proxy_parser.spiders" folder
        """
        self.path_to_file: Optional[str] = path_to_file
        self.proxy_limit: int = proxy_limit

        if scrapy_settings:
            self.settings: Optional[dict] = scrapy_settings
        else:
            self.settings: Optional[dict] = {
                "RETRY_TIMES": 10,
                "RETRY_HTTP_CODES": [500, 503, 504, 400, 403, 404, 408],
                "LOG_ENABLED": False
            }
        if path_to_file:
            self.settings["FEEDS"] = {
                path_to_file: {"format": path_to_file.split(".")[1]}
            }
            self.settings["FEED_EXPORT_ENCODING"] = "utf-8"
            self.settings["FEED_EXPORT_FIELDS"] = ["proxy"]
            self.settings["FEED_EXPORTERS"] = {
                "json": "proxy_parser.exporters.JsonExporter",
                "jsonlines": "proxy_parser.exporters.JsonLinesExporter",
            }

        self.spiders = [
            FreeProxyListSpider,
            BlogSpotSpider,
            ProxySearcherSpider,
            ProxySearcherSpider,
            HideMySpider,
        ]
        if scrapy_spiders:
            self.spiders.extend(scrapy_spiders)

    def parse(self) -> List[str]:
        """
        :return: List of verified proxies
        """
        self._write_to_file("start")
        dispatcher.connect(self._crawler_results, signal=signals.item_scraped)
        process = CrawlerProcess(settings=self.settings)
        for spider in self.spiders:
            process.crawl(spider)
        process.start()

        if self.proxy_limit:
            self.proxies = self.proxies[: self.proxy_limit]

        self._write_to_file("finish")
        return self.proxies

    def _write_to_file(self, action: str) -> None:
        if not self.path_to_file or self.path_to_file.startswith(("ftp", "s3", "gs")):
            return

        if action == "start":
            if self.path_to_file.endswith(".json"):
                with open(self.path_to_file, "wb") as file:
                    file.write(b"[")
            return

        if self.path_to_file.endswith(".json"):
            with open(self.path_to_file, "ab+") as file:
                file.truncate(file.tell() - 1)
                file.write(b"\n]")

    def _crawler_results(self, signal, sender, item, response, spider) -> None:
        self.proxies.append(item["proxy"])
