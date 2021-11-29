from abc import ABC, abstractmethod
from typing import Optional, List, Type

from scrapy import Spider


class ABCProxyParser(ABC):
    path_to_file: Optional[str]
    proxy_limit: int
    proxies: List[str]
    settings: Optional[dict]
    spiders: List[Type[Spider]]

    @abstractmethod
    def parse(self) -> List[str]:
        pass

    @abstractmethod
    def _crawler_results(self, signal, sender, item, response, spider) -> None:
        pass
