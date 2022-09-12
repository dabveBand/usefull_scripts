#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi el3arbi_@email.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------

from colorama import init
from colorama import Fore, Style

init()          # initialise Colorama (required for windows)
reset = Style.RESET_ALL     # reset colors to normal

BoldDim = Style.BRIGHT + Style.DIM
Bold = Style.BRIGHT

replace = {
    '*': '{1}({0}{2}{3}*{0}{1}){0}'.format(reset, BoldDim, BD, G),
    '+': '{1}({0}{2}+{0}{1}){0}'.format(reset, Dim, G),
    '!': '{1}({0}{2}!{1}){0}'.format(reset, BR, BO),
    '?': '{1}({0}{2}?{0}{1}){0}'.format(reset, BDim, G),
    '-': '{1}({0}{2}-{0}{1}){0}'.format(reset, OG, R),
}
