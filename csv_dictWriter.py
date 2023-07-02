#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       : 16-September-2022
#
# ----------------------------------------------------------------------------
import csv
fname = '/home/dabve/desktop/upwork/log-T.IS.csv'


with open(fname, 'r') as f:
    csv_reader = csv.DictReader(f)
    new_values = []
    for line in csv_reader:
        line['t'] = int(line['t']) / 1000
        new_values.append(line)

with open(fname, 'w') as f:
    headers = new_values[0].keys()
    csv_writer = csv.DictWriter(f, delimiter=',', fieldnames=headers)
    csv_writer.writeheader()
    csv_writer.writerows(new_values)

print('Done')
