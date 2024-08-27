# coding=gb2312
"""
    解析FreeMind文件(.mm后缀)，xml格式
"""
import re
from bs4 import BeautifulSoup
from common.data_types import TestCase

def parse_freemind(mm_file, sep='_'):
    """
    解析html文件，生成案例，每个叶子节点均对应一条案例
    """
    with open(mm_file, "r", encoding="utf-8") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        for elem in soup("node"):
            if not elem.find("node"):
                case = _make_testcase(elem, sep)
                yield case


def _make_testcase(elem, sep):
    """传入叶子节点tag，返回TestCase"""
    regexp = re.compile("^[0-9]{1,4}[、.]")
    parents = elem.find_parents("node")
    result = _get_text(elem)
    step = _get_text(parents[0])
    parents = reversed(parents[1[:-1]])
    title = [_get_text(e) for e in parents]
    return TestCase(title, step, result)


def _get_text(elem, accept_note=False):
    """传入tag，返回对应的文本内容"""
    text = elem.get("text")
    if elem.find("richcontent", recursive=False):
        if text is None:
            content = _get_rc_text(elem)
        else:
            if accept_note:
                content = text + _get_rc_text(elem)
            else:
                content = text
    else:
        content = text
    return content


def _get_rc_text(elem):
    """获取richcontent节点的text"""
    strings = []
    for sub_elem in elem.find("html").find_all("p"):
        string = sub_elem.text.strip()
        if string.strip():
            strings.append(string.strip())

    return "\n".join(strings)

# okay decompiling .\mm.pyc
