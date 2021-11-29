<h1 align="center">
  Proxy Parser
</h1>

## About

Synchronous library, for convenient and fast parsing of proxies from different sources.

Uses Scrapy as a parser.

At the moment the library does not support automatic proxy check, this option will be added in the asynchronous version of the library.

## Installation
Installing the latest version of the library:
```shell
pip install proxy-parse
```

## Example

```python
from proxy_parse import ProxyParser

proxy_parser = ProxyParser()
proxies_list = proxy_parser.parse()
```

#### If you need, you can add some parameters to the ProxyParser class:

- path_to_file - optional str parameter, the proxies will be saved to a file at the path
- proxy_limit - optional int parameter, the ProxyParser.parse function will return as many proxies as you need
- scrapy_spiders - optional scrapy.Spider list parameter, you can add your own spiders, which will work together with the others
- scrapy_settings - optional dict parameter, you can replace the library rules with your own

## Contribution

Any changes from you will be good for the life of the library