# encoding: utf-8
from __future__ import absolute_import

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models import (Model,
                              ForeignKey, ManyToManyField,
                              CharField, TextField,
                              DateField, IntegerField)
from django.utils.dateformat import format as date_format
from django.utils.translation import ugettext as _, pgettext, ugettext_lazy

from hvad.models import TranslatableModel, TranslatedFields

from slugify import slugify


class Author(Model):
    name = CharField(ugettext_lazy("Author Name"), max_length=100)
    slug = CharField(max_length=100, unique=True,
                     blank=True, null=True)
    birth_date = DateField(ugettext_lazy("Birth Date"),
                           blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)

        super(Author, self).save(*args, **kwargs)

    def __unicode__(self):
        if self.birth_date:
            # We'll be nice and use the active L10N format:
            b_date = date_format(settings.DATE_FORMAT, self.birth_date)
        else:
            b_date = pgettext("Birth Date", u"Unknown Date")

        fmt = pgettext("Author Profile", u"{name} ({birth_date})")

        return fmt.format(name=self.name, birth_date=b_date)


class Book(TranslatableModel):
    title = CharField(max_length=200)
    slug = CharField(ugettext_lazy("Unique identifier for use in URLs"),
                     max_length=200, unique=True,
                     blank=True, null=True)

    publication_date = DateField(blank=False)

    authors = ManyToManyField(Author, related_name="books")

    translations = TranslatedFields(description=TextField())

    def save(self, *args, **kwargs):
        if not self.slug and self.title:
            self.slug = slugify(self.title)

        super(Book, self).save(*args, **kwargs)

    def __unicode__(self):
        pub_date = date_format(settings.DATE_FORMAT, self.publication_date)
        return _("{title} ({publication_date})").format(title=self.title,
                                                        publication_date=pub_date)


class Review(TranslatableModel):
    book = ForeignKey(Book, related_name="reviews")
    user = ForeignKey('auth.User')

    created = DateField(auto_now_add=True)
    updated = DateField(auto_now=True, auto_now_add=True)

    rating = IntegerField(validators=[MinValueValidator(0),
                                      MaxValueValidator(5)])

    translations = TranslatedFields(review=TextField())

    class Meta:
        unique_together = (('book', 'user'), )

    def __unicode__(self):
        return _("Review of {book} by {user}").format(book=self.book,
                                                      user=self.user.username)
