# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

本底合并
"""


import numpy as np
import astropy.io.fits as fits
import logging
from .util import nowstr, mean_no_max

def combine_bias(
        bias_list:list[str], 
        master_bias_file:str,
        )->None:
    """
    将多个bias文件合并，生成一个master bias文件。
    """
    n_bias = len(bias_list)
    logging.info(f'combining {n_bias} bias files ...')
    # 打开第一个文件，获取头信息
    hdr = fits.getheader(bias_list[0])
    # 编写新的头信息
    hdr['NCOMBINE'] = n_bias
    hdr['COMBINED'] = 'YES'
    hdr['COMBDATE'] = nowstr()
    # 图像大小
    nx = hdr['NAXIS1']
    ny = hdr['NAXIS2']

    # 创建数组
    data_cube = np.empty((n_bias, ny, nx), dtype=np.float32)
    # 加载数据
    for i, filename in enumerate(bias_list):
        data_cube[i] = fits.getdata(filename)
    
    # 计算Pearson's emperical mode
    mean_data = 3 * np.median(data_cube, axis=0) - 2 * mean_no_max(data_cube)

    # 写入文件
    fits.writeto(master_bias_file, mean_data, hdr, overwrite=True)
