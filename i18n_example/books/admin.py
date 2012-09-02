# encoding: utf-8

from __future__ import absolute_import


from django.contrib.admin import site as admin_site, ModelAdmin

from hvad.admin import TranslatableAdmin
from modeltranslation.admin import TranslationAdmin


from .models import Author, Book, Review


class AuthorAdmin(TranslationAdmin):
    list_display = ('name', )
    prepopulated_fields = {"slug": ("name", )}

    class Media:
        js = (
            '/static/modeltranslation/js/force_jquery.js',
            'http://ajax.googleapis.com/ajax/libs/jqueryui/1.8.2/jquery-ui.min.js',
            '/static/modeltranslation/js/tabbed_translation_fields.js',
        )
        css = {
            'screen': ('/static/modeltranslation/css/tabbed_translation_fields.css', ),
        }


class BookAdmin(TranslatableAdmin):
    list_filter = ('publication_date', )
    prepopulated_fields = {"slug": ("title", )}


class ReviewAdmin(TranslatableAdmin):
    list_filter = ('book', 'user', 'rating')
    date_hierarchy = 'updated'


admin_site.register(Author, AuthorAdmin)
admin_site.register(Book, BookAdmin)
admin_site.register(Review, ReviewAdmin)
