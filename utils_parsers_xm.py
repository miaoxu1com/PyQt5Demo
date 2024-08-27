# coding=gb2312
"""
    解析XMind文件(.xmind后缀)
"""
import re
from xmindparser import xmind_to_dict
from common.data_types import TestCase

def _iter_xm_data():
    """解析XMind"""
    _row = []

    def inner(data):
        title = data.get("title")
        if title is not None:
            _row.append(title)
            topics = data.get("topics")
            if topics:
                for topic in topics:
                    yield from inner(topic)
                else:
                    _row.pop()

            else:
                yield _row
                _row.pop()

    return inner


def parse_xm(file: str, sep='_'):
    """
    解析XMind，每一行生成TestCase
    :param file:
    :param sep:
    :return: TestCase
    """
    xm_data = xmind_to_dict(file)
    first_canvas = xm_data[0]["topic"]
    for line in _iter_xm_data()(first_canvas):
        if len(line) > 2:
            *title, step, result = line
            yield TestCase(title, step, result)


if __name__ == "__main__":
    xm_file = "data/test.xmind"
    for i in parse_xm(xm_file):
        print(i)

