# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

平场合并
"""


import numpy as np
import astropy.io.fits as fits
import logging
from .util import nowstr

def combine_flat(
        master_bias:str|np.ndarray, 
        flat_list:list[str], 
        master_flat_file:str,
        )->None:
    """
    将多个flat文件合并，生成一个master flat文件。
    """
    # 加载master bias
    if isinstance(master_bias, str):
        master_bias = fits.getdata(master_bias)
    
    n_flat = len(flat_list)
    logging.info(f'combining {n_flat} flat files ...')

    # 打开第一个文件，获取头信息
    hdr = fits.getheader(flat_list[0])
    # 编写新的头信息
    hdr['NCOMBINE'] = n_flat
    hdr['COMBINED'] = 'YES'
    hdr['COMBDATE'] = nowstr()
    # 图像大小
    nx = hdr['NAXIS1']
    ny = hdr['NAXIS2']

    # 创建数组
    data_cube = np.empty((n_flat, ny, nx), dtype=np.float32)
    # 加载数据
    for i, filename in enumerate(flat_list):
        data_temp = fits.getdata(filename) - master_bias
        data_cube[i] = data_temp / np.median(data_temp)
    
    # 计算Pearson's emperical mode
    mean_data = 3 * np.median(data_cube, axis=0) - 2 * np.mean(data_cube, axis=0)

    # 写入文件
    fits.writeto(master_flat_file, mean_data, hdr, overwrite=True)
