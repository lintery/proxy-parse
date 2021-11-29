from scrapy.exporters import JsonItemExporter, JsonLinesItemExporter
from scrapy.utils.python import to_bytes


class JsonLinesExporter(JsonLinesItemExporter):
    def export_item(self, item):
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(to_bytes(itemdict["proxy"] + "\n", self.encoding))


class JsonExporter(JsonItemExporter):
    def _beautify_newline(self):
        if self.indent is not None:
            self.file.write(b"\n\t")

    def finish_exporting(self):
        self.file.write(b",")
        self.first_item = True

    def start_exporting(self):
        self._beautify_newline()

    def export_item(self, item):
        if self.first_item:
            self.first_item = False
        else:
            self.file.write(b",")
            self._beautify_newline()
        itemdict = dict(self._get_serialized_fields(item))
        self.file.write(b'"' + to_bytes(itemdict["proxy"], self.encoding) + b'"')
