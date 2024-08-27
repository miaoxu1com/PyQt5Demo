# coding=gb2312
from pathlib import Path


def get_all_files(directory):
    # 创建一个 Path 对象
    dir_path = Path(directory)

    # 使用 rglob() 方法递归地获取目录下的所有文件
    files = dir_path.rglob('*')

    # 返回生成器中的所有文件
    return files


def get_dirs_realpath(directory=Path.cwd()):
    directory = Path(directory)
    file_paths = [f.resolve() for f in directory.iterdir() if f.is_file()]
    temp_path = file_paths[0]
    return temp_path
