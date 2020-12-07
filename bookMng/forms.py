from django import forms
from django.forms import ModelForm
from .models import Book, Review, RecommendedBook


class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = {
            'name',
            'web',
            'price',
            'picture'
        }


class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = {
            'name',
            'email',
            'body'
        }


class BookForm(ModelForm):
    class Meta:
        model = RecommendedBook
        fields = {
            'name',
            'web',
            'price',
            'picture'
        }
