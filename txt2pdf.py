#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# author        : el3arbi bdabve@gmail.com
# created       :
#
# description   :
# usage         :
# ----------------------------------------------------------------------------


import click
from fpdf import FPDF


@click.command()
@click.argument('input_file', type=click.Path(exists=True))
@click.argument('output_file')
def convert_to_pdf(input_file, output_file):
    with open(input_file, 'r') as file:
        text = file.read()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, text)

    pdf.output(output_file)
    click.echo(f'Done writing to: {output_file}')


if __name__ == '__main__':
    convert_to_pdf()
