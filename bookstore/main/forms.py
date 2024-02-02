from django import forms
from .models import Book

PRODUCT_CATEGORY = list()

for i in range(Book.objects.all().count()):
    PRODUCT_CATEGORY.append((i, Book.objects.all()[i].title))

class AddProductForm(forms.Form):
    title = forms.CharField(max_length=60)
    price = forms.IntegerField()
    book_covers = forms.ImageField(required=False)
    description = forms.CharField()
    category = forms.TypedChoiceField(choices=PRODUCT_CATEGORY, coerce=str)

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'publisher', 'description', 'price', 'cover_image']
