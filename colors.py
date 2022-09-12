#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    :
# desc    : terminal colors without third packege; all terminal colors in '/home/dabve/bin/lib/cliColor'
# -------------------------------------------------------------------------------------------------------


class Colors(object):
    """
    Create color instance; then use color name
    color = Colors()
    color.BD
    """
    reset = '\033[0m'  # white (normal)
    BD = '\033[1m'     # Bold
    Underline = '\033[4m'    # Underline
    Dim = '\033[2m'      # dims current color.
    BDim = '\033[1m\033[2m'
    # BD, Underline, Dim must be reseted with reset

    R = '\033[31m'    # red
    G = '\033[32m'    # green
    OG = '\033[33m'    # orange
    B = '\033[34m'    # blue
    P = '\033[35m'    # purple
    C = '\033[36m'    # cyan
    GR = '\033[37m'   # gray

    BR = '\033[1;31m'    # red
    BG = '\033[1;32m'    # green
    BO = '\033[1;33m'    # orange
    BB = '\033[1;34m'    # blue
    BP = '\033[1;35m'    # purple
    BC = '\033[1;36m'    # cyan
    BGR = '\033[1;37m'   # gray

    DimR = '\033[2;31m'    # red
    DimG = '\033[2;32m'    # green
    DimO = '\033[2;33m'    # orange
    DimB = '\033[2;34m'    # blue
    DimP = '\033[2;35m'    # purple
    DimC = '\033[2;36m'    # cyan
    DimGR = '\033[2;37m'   # gray

    replace = {
        '*': '{1}({0}{2}{3}*{0}{1}){0}'.format(reset, BDim, BD, G),
        '+': '{1}({0}{2}+{0}{1}){0}'.format(reset, Dim, G),
        '!': '{1}({0}{2}!{1}){0}'.format(reset, BR, BO),
        '?': '{1}({0}{2}?{0}{1}){0}'.format(reset, BDim, G),
        '-': '{1}({0}{2}-{0}{1}){0}'.format(reset, OG, R),
    }

    def bold_msg(self, msg):
        return '{}{}{}'.format(self.BD, msg, self.reset)

    def boldgreen_msg(self, msg):
        return '{}{}{}'.format(self.BG, msg, self.reset)

    def error_msg(self, msg):
        return '\n{} {}{}{}\n'.format(self.replace['-'], self.R, msg, self.reset)

    def simple_msg(self, msg):
        return '{} {}'.format(self.replace['+'], msg)

    def title_msg(self, msg):
        return '{} {}{}{}'.format(self.replace['*'], self.BD, msg, self.reset)

    def input_msg(self, msg):
        return '{} {}{}{}'.format(self.replace['?'], self.G, msg, self.reset)

    def info_msg(self, msg):
        return '{} {}{}{}'.format(self.replace['!'], self.OG, msg, self.reset)


if __name__ == '__main__':
    # usage
    color = Colors()
    print(color.__doc__)
    print(color.BD + 'Bold' + color.reset + ' White ' + color.Underline + 'Underline' + color.reset, end='')
    print(color.Dim + ' Dim' + color.reset)
    print()
    print(color.R + 'Red' + color.C + ' Cyan' + color.B + ' Blue' + color.G + ' Green', end='')
    print(color.P + ' Purple' + color.GR + ' Gray' + color.OG + ' Orange')
    print()
    print(color.BR + 'RedBold' + color.BC + ' CyanBold' + color.BB + ' BlueBold', end='')
    print(color.BG + ' GreenBold', end='')
    print(color.BP + ' PurpleBold' + color.BGR + ' GrayBold' + color.BO + ' OrangeBold')
    print(color.reset)

    print(color.DimR + 'RedDim' + color.DimC + ' CyanDim' + color.DimB + ' BlueDim', end='')
    print(color.DimG + ' GreenDim', end='')
    print(color.DimP + ' PurpleDim' + color.DimGR + ' GrayDim' + color.DimO + ' OrangeDim')
    print(color.reset)

    print()
    print(color.replace['-'], 'Error')
    print(color.replace['+'], 'Message')
    print(color.replace['!'], 'Alert')
    print(color.replace['*'], 'Title')
    print()
    print(color.title_msg('Domain Info:'))
    print(color.simple_msg('Please Wait...'))
    print(color.error_msg('Type Error'))
    input_ = input(color.input_msg('Data To Parse: '))
    print(input_)
