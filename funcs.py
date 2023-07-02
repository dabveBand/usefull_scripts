#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# file    :
# desc    : important functions
# ---------------------------------------------------------

import csv
from collections import namedtuple


def csv_2_namedTuple(fname, delimiter=','):
    # from csv files to a namedTuple
    with open(fname) as csv_f:
        csv_reader = csv.reader(csv_f, delimiter=delimiter)
        headings = next(csv_reader)
        Row = namedtuple('Row', headings)
        rows = [Row(*line) for line in csv_reader]
        return rows


if __name__ == '__main__':
    rows = csv_2_namedTuple('../../desktop/data.csv', ',')
    fields = [row._fields for row in rows][0]
    as_dict = [row._asdict() for row in rows]
    for row in rows:
        print(row)
