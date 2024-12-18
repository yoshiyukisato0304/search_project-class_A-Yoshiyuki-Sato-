from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Category
from .forms import ProductForm, SearchForm, ProductCompareForm
from django.core.paginator import Paginator
from django.shortcuts import render

def product_create(request):
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES,)
        if form.is_valid():#フォームが有効かの確認.
            product = form.save(commit=False)
            product.createuser = request.user  # ログインしているユーザーをセット.
            product.save()  # 保存.
            return redirect('search_app:search_view')
    else:
        form = ProductForm()
        return render(request, 'search_app/product_form.html', {'form': form})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'search_app/product_detail.html', {'product': product})


def product_update(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            form.save()
            return redirect('search_app:product_detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    # product オブジェクトをテンプレートに渡す
    return render(request, 'search_app/product_form.html', {'form': form, 'product':
    product})
    43


def product_delete(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.delete()
        return redirect('product_list')
    return render(request, 'search_app/product_confirm_delete.html', {'product': product})


def product_list(request):
    products = Product.objects.all()
    return render(request, 'search_app/product_list.html', {'products': products})


def search_view(request):

    form = SearchForm(request.GET or None)
    results = Product.objects.all() # クエリセットの初期化
    if form.is_valid():
        query = form.cleaned_data['query']
        if query:
            results = results.filter(name__icontains=query) # ここでの filter はクエリセットに適用
    
    # カテゴリフィルタリング
    category_name = request.GET.get('category')
    if category_name:
        try:
    # カテゴリ名に基づいてカテゴリ ID を取得
            category = Category.objects.get(name=category_name)
            results = results.filter(category_id=category.id)
        except Category.DoesNotExist:
            results = results.none() # 存在しないカテゴリの場合、結果を空にする
            category = None

    # 価格のフィルタリング（最低価格・最高価格） 
    min_price = request.GET.get('min_price') 
    max_price = request.GET.get('max_price') 
    if min_price: 
        results = results.filter(price__gte=min_price) 
    if max_price: 
        results = results.filter(price__lte=max_price) 

    sort_by = request.GET.get('sort', 'name') 
    if sort_by == 'price_asc': 
        results = results.order_by('price') 
    elif sort_by == 'price_desc': 
        results = results.order_by('-price') 
    else:
        results = results.order_by('name')  # デフォルトの並び替え
 
    # クエリセットをリストに変換せず、直接 Paginator に渡す
    paginator = Paginator(results, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
 
    return render(request, 'search_app/search.html', {'form': form, 'page_obj': page_obj})



def favorite_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if product in request.user.favorite_place.all():
        request.user.favorite_place.remove(product)
    else:
        request.user.favorite_place.add(product)
    return redirect('search_app:product_detail', pk=product.id)

def favorite_list(request):
    favorite_products = request.user.favorite_place.all()
    return render(request, 'search_app/favorite_list.html', {'favorite_products': favorite_products})

def compare_products(request):
    if request.method == 'POST':
        form = ProductCompareForm(request.POST)
        if form.is_valid():
            product1 = form.cleaned_data['product1']
            product2 = form.cleaned_data['product2']
            context = {
                'product1': product1,
                'product2': product2,
            }
            return render(request, 'search_app/compare_result.html', context)
    else:
        form = ProductCompareForm()

    return render(request, 'search_app/compare_choice.html', {'form': form})