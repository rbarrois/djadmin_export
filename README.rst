This Django application provides export functionality to all tables in Django's admin.

Installation
============

First, you need to install the ``djadmin_export`` module:

- Through pip::

    $ pip install djadmin_export

- From sources::

    $ git clone git@github.com/rbarrois/djadmin_export.git
    $ cd djadmin_export
    $ python setup.py install


Activation
==========

Once you have installed ``djadmin_export``,
you need to activate it on your project.

The simplest way is to add the following lines to your ``urls.py`` file:

.. sourcecode:: python

    from djadmin_export import register
    register.auto_register_exporters()

You must now declare, in your ``settings.py`` file, which exporter you wish
to install:

.. sourcecode:: python

    ADMIN_EXPORTERS = (
        'djadmin_export.exporters.xlsx.XLSXExporter',
    )


Dependencies
============

In itself, ``djadmin_export`` only relies on a recent enough version of ``Django`` (1.8, 1.10 or 1.11).

Each exporter may have specific dependencies:

- ``XLSXExporter`` requires the ``openpyxl`` package


Links
=====

- Issues: https://github.com/rbarrois/djadmin_export/issues/
- Source code: https://github.com/rbarrois/djadmin_export/
- Doc: http://djadmin_export.readthedocs.org/
- PyPI: http://pypi.python.org/pypi/djadmin_export/
