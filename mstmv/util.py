# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

本模块用于提供常用函数
"""


import numpy as np
import os


def nowstr()->str:
    """
    返回当前时间字符串，格式为：20241212_123456
    """
    from datetime import datetime
    return datetime.now().strftime("%Y-%m-%dT%H:%M:%S")


def mean_no_max(cube:np.ndarray)->np.ndarray:
    """
    计算平均值，不包含最大值
    """
    return (np.sum(cube, axis=0) - np.max(cube, axis=0)) / (cube.shape[0]-1)


def tqdm_bar(total, task):
    """genreate a tqdm progress-bar with default format"""
    from tqdm import tqdm
    return tqdm(total=total, bar_format=
        task + ':{l_bar}{bar}| {n:3d}/{total:3d} [{elapsed}/{remaining}]')


def basename(filename:str)->str:
    """
    从文件路径列表中提取文件名
    """
    return os.path.splitext(os.path.basename(filename))[0]
