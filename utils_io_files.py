# coding=gb2312
from pathlib import Path
import codecs

def read(file, mode='r', encoding='utf-8'):
    with open(file, mode, encoding=encoding) as fp:
        return fp.read()


def add_bom_utf8(file):
    path = Path(file)
    data = path.read_bytes()
    if not data.startswith(codecs.BOM_UTF8):
        path.write_bytes(codecs.BOM_UTF8 + data)


def encoding_to(file, old='gb2312', new='utf-8', with_bom=False):
    """按old方式解码，重新按new方式编码"""
    with open(file, "rb") as fp:
        data = fp.read().lstrip(codecs.BOM_UTF8)
    try:
        data = data.decode(old)
    except UnicodeError:
        pass
    else:
        if with_bom:
            if new.lower() in ('utf8', 'utf-8', 'utf_8'):
                data = codecs.BOM_UTF8.decode("utf-8") + data
        with open(file, "w", encoding=new, newline="") as fp:
            fp.write(data)
