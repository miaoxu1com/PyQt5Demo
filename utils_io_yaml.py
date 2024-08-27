# coding=gb2312
from collections import OrderedDict
import yaml

def load(yaml_path, *, loader=yaml.Loader, object_pairs_hook=OrderedDict, encoding="utf-8"):
    """ordered_yaml_load，反序列化，有序读取yaml文件"""

    class OrderedLoader(loader):
        pass

    def construct_mapping(_loader, node):
        _loader.flatten_mapping(node)
        return object_pairs_hook(_loader.construct_pairs(node))

    OrderedLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
    with open(yaml_path, encoding=encoding) as fp:
        return yaml.load(fp, OrderedLoader)


def dump(data, yaml_path, *, dumper=yaml.SafeDumper, encoding="utf-8", **kwds) -> None:
    """ordered_yaml_dump，序列化，有序写入yaml文件"""

    class OrderedDumper(dumper):
        pass

    def _dict_representer(_dumper, _data):
        return _dumper.represent_mapping(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _data.items())

    OrderedDumper.add_representer(OrderedDict, _dict_representer)
    with open(yaml_path, "w", encoding=encoding) as fp:
        (yaml.dump)(data, fp, OrderedDumper, **kwds)


def read(file, encoding='utf-8'):
    return load(file, encoding=encoding)


def write(file, data, encoding='utf-8'):
    dump(data, file, encoding=encoding, allow_unicode=True)
