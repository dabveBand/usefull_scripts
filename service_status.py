#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    :
# desc    : check if service is Active
# ------------------------------------

from subprocess import Popen, PIPE


def service_st(s_name):
    """
    # usage service_st(s_name)
    # return True if service is active; else False; error if errors
    """
    if not s_name:
        s_name = input('(?) service name: ')
    cmd = ['service', s_name, 'status']
    exec_cmd = Popen(cmd, stdout=PIPE, stderr=PIPE)
    out, err = exec_cmd.communicate()
    if err:
        print('(-) Error: {}'.format(err.decode('utf8')))
        exit()
    else:
        for line in str(out).split('\\n'):
            line = str(line).strip()
            if line.startswith('Active:'):
                st = line.split()[-2]
                if st == 'inactive':
                    return False
                else:
                    return True


if __name__ == '__main__':
    print(service_st('gnome'))
