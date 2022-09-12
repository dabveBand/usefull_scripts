#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# /----------------------------------------------------------------------------
#
#          FILE: pdfCutPages.py
#
#         USAGE: ./pdfCutPages.py -f <PDF file name> -r <'Range of pages to cut separated by ,'> -o <output>
#                ./pdfCutPages.py -f input.pdf -r '15,20' -o output.pdf
#   DESCRIPTION: Cut pages from a pdf file and save them in another pdf file
#
#        AUTHOR: daBve (), dabve@outlook.fr
#       CREATED: 03-Sep-2017
#
# \----------------------------------------------------------------------------
import click


@click.command()
@click.option('-f', '--input-file', 'pdf_in', help='Specify PDF name for input')
@click.option('-r', '--page-range', 'page_range', nargs=2, type=int, help='Specify Range of pages to cut separated by space')
@click.option('-o', '--out-file', 'pdf_out', help='Specify PDF file name for output')
def writeToPdf(pdf_in, page_range, pdf_out):
    with open(pdf_in, 'rb') as pdf_input:
        pdf_reader = PyPDF2.PdfFileReader(pdf_input, 'rb')
        pdf_writer = PyPDF2.PdfFileWriter()

        print('[*] This PDF Contain: {} pages'.format(pdf_reader.numPages))
        print('[+] Writing pages to: {} '.format(pdf_out))
        beg, end = page_range
        for page_num in range(beg, end):
            page_obj = pdf_reader.getPage(page_num)
            print(page_obj.extractText())
            pdf_writer.addPage(page_obj)            # adding pages to the writer

        with open(pdf_out, 'wb') as pdf_outf:
            # write page to pdf out
            pdf_writer.write(pdf_outf)
            print('[+] Done writing')


if __name__ == '__main__':
    import PyPDF2
    writeToPdf()
