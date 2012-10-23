# -*- coding: utf-8 -*-
# Copyright (c) 2012 Raphaël Barrois
# This code is distributed under the LGPLv3 License.


from django.conf import settings
from django.contrib.admin import site as default_admin_site
from django.utils import importlib


def load_exporter(exporter):
    """Load an exporter, importing it if needed.

    This takes either an exporter class or its fully qualified name.
    """
    if isinstance(exporter, str):
        # Got a module name, import it.
        module_name, class_name = exporter.rsplit('.', 1)
        module = importlib.import_module(module_name)
        exporter = getattr(module, class_name)
    return exporter


def register_exporter(exporter, admin_site=None):
    """Register an exporter to an admin site.

    Args:
        - exporter: may be an Exporter class or its fully qualified name.
        - admin_site: a django.contrib.admin.sites.AdminSite instance; if None,
            the default at ``admin.site`` will be used.
    """
    admin_site = admin_site or default_admin_site
    exporter_class = load_exporter(exporter)

    name = exporter_class.get_name()
    admin_site.add_action(exporter_class.to_action(), name=name)


def register_exporters(*exporters, **kwargs):
    admin_site = kwargs.get('admin_site')
    for exporter in exporters:
        register_exporter(exporter, admin_site)


def auto_register_exporters(admin_site=None):
    """Automatically register all exporters defined in settings.
    
    This relies on the ADMIN_EXPORTERS section.
    """
    for exporter in getattr(settings, 'ADMIN_EXPORTERS', ()):
        register_exporter(exporter, admin_site)
