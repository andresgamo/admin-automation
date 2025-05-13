"""Multipart parser"""

import io
from multipart import MultipartParser


def parse_multipart(event):
    body = event["body"].encode("utf-8")
    content_type = event["headers"].get("Content-Type")
    boundary = content_type.split("boundary=", 1)[1].replace('"', "")
    parser = MultipartParser(io.BytesIO(body), boundary)
    return {part.name: part for part in parser}
