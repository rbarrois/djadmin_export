from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from djadmin_export import register
register.auto_register_exporters()

urlpatterns = patterns('',
    url(r'^', include(admin.site.urls)),
)
