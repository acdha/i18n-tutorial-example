# encoding: utf-8
from __future__ import absolute_import

from django.conf.urls import patterns, include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from .books.views import BookList, BookDetail

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls))
)

urlpatterns += i18n_patterns('',
    url(r'^book/$', BookList.as_view(), name='book-list'),
    url(r'^book/(?P<slug>[^/]+)/$', BookDetail.as_view(), name='book-detail'),
)

urlpatterns += staticfiles_urlpatterns()
