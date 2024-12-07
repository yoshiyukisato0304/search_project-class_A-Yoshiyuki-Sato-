from django import forms
from .models import Product

class SearchForm(forms.Form):
    query = forms.CharField(
    label='検索キーワード',
    max_length=100, # CharField で max_length が有効です
    required=False,
    widget=forms.TextInput(attrs={'placeholder': '検索したいキーワードを入力'}))
    

class ProductForm(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'price', 'image', 'category']

        exclude = ['createuser']

class ProductCompareForm(forms.Form):
    product1 = forms.ModelChoiceField(queryset=Product.objects.all(), label="商品1")
    product2 = forms.ModelChoiceField(queryset=Product.objects.all(), label="商品2")