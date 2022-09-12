#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# DESC     : how to deal with images from python from automate the boring stuff oh_my
# ------------------------------------------------------------------------------
from PIL import Image
item = Image.open('./photos_1410023014500.jpg')
item.size
item.filename
item.format
item.format_description
item.save('elhadj.jpg')

# new image
im = Image.new('RGBA', (100, 200), 'purple')
im.save('purpleImage.png')
im_2 = Image.new('RGBA', (20, 20))
im_2.save('transparentImage.png')
croppedIm = item.crop((335, 345, 565, 560))
croppedIm.save('croppedIm.png')

# resizing image
width, height = item.size
quarterSizedImage = item.resize((int(width / 2), int(height / 2)))
quarterSizedImage.save('elhadj_resized.png')

from PIL import ImageDraw, ImageFont
import os
im = Image.new('RGBA', (200, 200), 'white')
draw = ImageDraw.Draw(im)
draw.text((20, 150), 'Hello From Python', fill='purple')
im.save('text.png')

fontsFolder = 'FONT_FOLDER'         # e.g. ‘/Library/Fonts’
arialFont = ImageFont.truetype(os.path.join(fontsFolder, 'arial.ttf'), 32)
draw.text((100, 150), 'Howdy', fill='gray', font=arialFont)
im.save('text.png')
