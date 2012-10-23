# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois
# This code is distributed under the LGPLv3 License.


import openpyxl
import tempfile

from django.utils.functional import Promise

from . import base


class ExportWorkBook(object):
    def __init__(self):
        self.book = openpyxl.Workbook(optimized_write=True)
        self.sheet = self.book.create_sheet()

    def set_title(self, title):
        title = unicode(title)
        if len(title) >= 32:
            raise ValueError("An excel sheet title cannot be longer than 32 chars.")
        self.sheet.title = title

    def fill(self, rows, headers=None):
        """Fill an excel sheet with data.

        Args:
            rows (object list list): the list of rows to inserts
            headers (unicode list): the title of columns
        """
        if headers:
            headers = [unicode(header) for header in headers]
            self.sheet.append(headers)

        for row in rows:
            self.sheet.append(row)

        if headers:
            self.sheet.auto_filter = self.sheet.calculate_dimension()

    def write_to_file(self, f):
        """Write the content of the WorkBook to an existing file."""
        with tempfile.NamedTemporaryFile(suffix='.xlsx') as tmp_file:
            self.book.save(tmp_file.name)
            f.write(tmp_file.read())


class XLSXExporter(base.BaseExporter):
    content_type = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    extension = 'xlsx'

    def normalize_value(self, value):
        if isinstance(value, Promise):
            # Force evaluation of lazy objects
            return unicode(value)
        return value

    def fill_file(self, f, columns):
        # Excel sheet titles are limited to 32 chars
        title = self.make_title()[:32]
        headers = [title for _name, title in columns]
        rows = self.rows(columns)

        book = ExportWorkBook()
        book.fill(rows, headers)
        book.set_title(title)
        book.write_to_file(f)
