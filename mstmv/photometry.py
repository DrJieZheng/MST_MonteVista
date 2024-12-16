# -*- coding: utf-8 -*-

"""
MonteVista: A pipeline for processing MiniSiTian data
packagename: mstmv
By Dr Jie Zheng
v0 20241212

找源和测光
"""


import os
import subprocess
import numpy as np
import astropy.io.fits as fits
import logging
from .util import tqdm_bar


def photometry(
        img_list:list[str], 
        out_dir:str,
        )->None:
    """
    对改正后的图像进行找源和测光，使用Source-Extractor
    """
    # check installation of se
    if os.system(f"which sex > /dev/null") == 0:
        se_cmd = "sex"
    elif os.system(f"which source-extractor > /dev/null") == 0:
        se_cmd = "source-extractor"
    elif os.system(f"which sextractor > /dev/null") == 0:
        se_cmd = "sextractor"
    else:
        raise OSError("No Source-Extractor Installed")
    # 找到当前程序所在路径
    here = os.path.dirname(__file__)
    # se_command and parameters, use local if exists
    if os.path.isfile("default.sex"):
        se_conf = "default.sex"
    else:
        se_conf = os.path.join(here, 'default.sex')
    se_par = os.path.join(here, 'default.param')
    logging.info(f"SE {se_cmd} {se_conf}")

    n_img = len(img_list)
    logging.info(f'photometry {n_img} images ...')
    pbar = tqdm_bar(n_img, "Photometry")
    for i, filename in enumerate(img_list):
        bn = os.path.splitext(os.path.basename(filename))[0]
        corr_file = os.path.join(out_dir, bn + '_corr.fits')
        secat_file = os.path.join(out_dir, bn + '_cat.fits')
        subprocess.run([se_cmd, "-c", se_conf, corr_file, "-CATALOG_NAME", secat_file],
            stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True, shell=False, 
            executable=None, text=False, bufsize=-1, timeout=None,)
        pbar.update(1)
    pbar.close()

