# encoding: utf-8
"""
django-modeltranslation configuration

See http://code.google.com/p/django-modeltranslation/wiki/InstallationAndUsage#Registering_models_and_their_fields_for_translation
"""
from __future__ import absolute_import

from modeltranslation.translator import TranslationOptions, translator

from i18n_example.books.models import Author


class AuthorTranslationOptions(TranslationOptions):
    fields = ('name', )

    group_fields = True
    use_tabs = True

translator.register(Author, AuthorTranslationOptions)
