# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

本底平场改正
"""


import os
import numpy as np
import astropy.io.fits as fits
import logging
from .util import nowstr, tqdm_bar, basename


def correct_img(
        master_bias:str|np.ndarray, 
        master_flat:str|np.ndarray, 
        img_list:list[str], 
        out_dir:str,
        )->None:
    """
    对图像列表进行bias和flatfield校正。
    """
    # 加载master bias
    if isinstance(master_bias, str):
        master_bias = fits.getdata(master_bias)
    if isinstance(master_flat, str):
        master_flat = fits.getdata(master_flat)

    n_img = len(img_list)
    logging.info(f'correcting {n_img} images ...')
    pbar = tqdm_bar(n_img, "Correcting")
    for i, filename in enumerate(img_list):
        bn = os.path.splitext(os.path.basename(filename))[0]
        corr_file = os.path.join(out_dir, bn + '_corr.fits')
        # 读取图像和头
        data = fits.getdata(filename)
        hdr = fits.getheader(filename)
        # 减去bias，除以flat
        data = (data - master_bias) / master_flat
        # 头部
        hdr['CORRDATE'] = nowstr()
        # 写入文件
        fits.writeto(corr_file, data, hdr, overwrite=True)
        pbar.update(1)
    pbar.close()
