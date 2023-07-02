#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 10-November-2022
#
# description   : barcode reader
# ----------------------------------------------------------------------------

import cv2
from pyzbar.pyzbar import decode


def barcode_reader(image):
    img = cv2.imread(image)         # return a numpy tuple
    decoded_objects = decode(img)   # decode the code bar
    for obj in decoded_objects:
        print('[*] Detected barcode: \n{}\n'.format(obj))
        print('[+] Type        : {}'.format(obj.type))
        print('[+] Data        : {}'.format(obj.data))
        print('[+] Orientation : {}'.format(obj.orientation))
        print('[+] Quality     : {}'.format(obj.quality))
        print('-' * 30)


if __name__ == '__main__':
    for f in ['./elio_barcode.png', './barcode1.png', './barcode2.jpeg', './bar_.jpg']:
        barcode_reader(f)
