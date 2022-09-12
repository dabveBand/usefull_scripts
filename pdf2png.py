#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    : pdf2png.py
# caller  : main
# author  : Ibrahim Addadi; dabve@gmail.com.
# created : 25-December-2020
# version : 0.1.0
# desc    : take a pdf as input and convert all pages to a .png files
# ---------------------------------------------------------

from pdf2image import convert_from_path

pdf_in = convert_from_path('~/python/project/eljoumou3a/eljoumou3a/static/sahih_bukhari/1_(1_7)_كتاب_بدء_الوحي.pdf')
out_dir = '~/python/project/eljoumou3a/eljoumou3a/static/sahih_bukhari'

index = 1
for img in pdf_in:
    out_name = '{}{}.{}'.format(out_dir, index, 'png')
    img.save(out_name)
    index += 1
