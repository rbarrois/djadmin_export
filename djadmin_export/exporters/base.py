# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois
# This code is distributed under the LGPLv3 License.


import datetime

from django.http import HttpResponse
from django.utils.translation import ugettext_lazy as _

from .. import utils


class ExportAction(object):
    """An admin action for exporting files."""
    def __init__(self, exporter_class):
        self.exporter_class = exporter_class
        self.short_description = exporter_class.get_description()

    def _collect_options(self, modeladmin):
        """Collect export options from the ModelAdmin definition."""
        return {
            'columns': getattr(modeladmin, 'export_columns', None),
            'exclude_columns': getattr(modeladmin, 'export_exclude_columns', None),
        }

    def __call__(self, modeladmin, request, queryset):
        """Actually perform the action: export the selected queryset."""
        options = self._collect_options(modeladmin)
        exporter = self.exporter_class(queryset, **options)
        return exporter.export_to_response()


class BaseExporter(object):
    """The basis for all file exporters.

    Class attributes:
        content_type (str): the MIME type to use when sending the file
        extension (str): the extension to use for such files
        readable_file_kind (str): the "human-readable" kind of files

    Attributes:
        queryset (QuerySet): the admin-originating QuerySet
        model (Model): the model being extracted
        options (dict): extra options extracted freely provided
    """

    content_type = 'application/octet-stream'
    extension = 'dat'
    readable_file_kind = ''

    @classmethod
    def get_description(cls):
        """Retrieve the description of this exporter."""
        readable_file_kind = cls.readable_file_kind or cls.extension
        return _(u"Export selected objects as a %s file") % readable_file_kind

    @classmethod
    def get_name(cls):
        return cls.__name__.lower()

    @classmethod
    def to_action(cls):
        """Build an ExportAction from this exporter."""
        return ExportAction(cls)

    def __init__(self, queryset, **export_options):
        self.queryset = queryset
        self.model = queryset.model
        self.options = export_options

    def make_filename(self):
        """Build a filename for the current model/queryset combination."""
        base = utils.slugify(self.model._meta.verbose_name_plural)
        return '%s_%s.%s' % (base, datetime.date.today(), self.extension)

    def make_title(self):
        """Build a title for the current queryset."""
        return unicode(self.model._meta.verbose_name)

    def get_column_title(self, name):
        """Return the title of a column, as a (lazy) unciode object."""
        return self.model._meta.get_field(name).verbose_name

    def get_columns(self):
        """Retrieve the list of (name, title) of selected columns.

        If a list of 'export_columns' has been given, uses it; otherwise, uses
        the list of fields defined on the model.
        """
        columns = self.options.get('columns')
        if not columns:
            columns = [f[0].name for f in self.model._meta.get_fields_with_model()]
        exclude_columns = self.options.get('exclude_columns')
        if exclude_columns:
            columns = [column for column in columns if column not in exclude_columns]

        return [(column, self.get_column_title(column)) for column in columns]

    def get_value(self, entry, column):
        """Get a field value on an entry.

        Will use get_FOO_display() if available.
        """
        try:
            value = getattr(entry, 'get_%s_display' % column)()
        except AttributeError:
            value = getattr(entry, column)
        return self.normalize_value(value)

    def normalize_value(self, value):
        """Extension point for custom value normalization."""
        return value

    def entry_to_row(self, entry, columns):
        """Convert a QuerySet entry to a row."""
        row = []
        for name, _title in columns:
            row.append(self.get_value(entry, name))
        return row

    def rows(self, columns):
        """Convert the queryset to a list of rows."""
        for entry in self.queryset.iterator():
            yield self.entry_to_row(entry, columns)

    def fill_file(self, f, columns):
        """Actually fill the file."""
        raise NotImplementedError()

    def prepare_response(self):
        """Prepare the HttpResponse object."""
        response = HttpResponse(content_type=self.content_type)
        response['Content-Disposition'] = 'attachment; filename=%s' % self.make_filename()
        return response

    def export_to_response(self):
        """Export the queryset to a HttpResponse object."""
        response = self.prepare_response()
        self.export_to_file(response)
        return response

    def export_to_file(self, filelike):
        """Export the queryset to an open file-like object."""
        columns = self.get_columns()
        self.fill_file(filelike, columns)
