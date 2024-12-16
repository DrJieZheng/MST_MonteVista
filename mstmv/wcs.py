# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

天测定标
"""


import os
# import subprocess
import numpy as np
import astropy.io.fits as fits
import logging
from .util import tqdm_bar


def photometry(
        img_list:list[str], 
        )->None:
    """
    基于找源结果，进行手工天测
    """

    n_img = len(img_list)
    logging.info(f'astrometry {n_img} images ...')
    pbar = tqdm_bar(n_img, "Astrometry")
    for i, filename in enumerate(img_list):
        basename = os.path.splitext(os.path.basename(filename))[0]
        secat_file = os.path.splitext(filename)[0] + '_cat.fits'
        wcs_file = os.path.splitext(filename)[0] + '_wcs.hdr'
        
        pbar.update(1)
    pbar.close()

