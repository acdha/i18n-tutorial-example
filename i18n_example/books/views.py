# encoding: utf-8
from __future__ import absolute_import

from django.db.models import Avg, Count
from django.views.generic import DetailView, ListView
from django.template.response import TemplateResponse

from .models import Book


class BookList(ListView):
    model = Book


class BookDetail(DetailView):
    model = Book

    def get_queryset(self):
        qs = Book.objects.all()

        qs = qs.annotate(average_rating=Avg("reviews__rating"),
                         rating_count=Count("reviews"))

        return qs

    def get_context_data(self, **kwargs):
        context = super(BookDetail, self).get_context_data(**kwargs)
        context['lang_reviews'] = self.object.reviews.language(self.request.LANGUAGE_CODE)
        return context