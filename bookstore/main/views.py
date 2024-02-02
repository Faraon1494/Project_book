from django.shortcuts import render, redirect, get_object_or_404
from .models import Book, Category
from cart.forms import CartAddProductForm, CartNewProductForm
from main.forms import AddProductForm
from .forms import BookForm
from django.contrib.gis.geoip2 import GeoIP2
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from django.http import HttpResponseForbidden

# Create your views here.
# @cache_page(60 * 15)
def index(request):
    try:
        items_cahce = cache.get("items_cache")
    except:
        items_cahce=Book.objects.all()
        cache.set("items_cache", items_cahce, 600)
    g = GeoIP2(settings.GEOIP_PATH)
    # g.country(request.META.get('REMOTE_ADDR'))
    # 149.115.178.2 - ip адрес, который есть в базе
    a = g.country('149.115.178.2') # запрос к базе с данным айпи адресом
    print(request.META.get('REMOTE_ADDR')) # адрес пользователя
    print(a['country_name']) # вывод страны пользователя
    selected_category = request.GET.get('category')
    author_query = request.GET.get('author')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    sort_by = request.GET.get('sort_by', 'title')
    title_query = request.GET.get('title')

    items = Book.objects.all()


    if selected_category:
        items = items.filter(category__name=selected_category)
    if min_price:
        items = items.filter(price__gte=min_price)
    if max_price:
        items = items.filter(price__lte=max_price)

    if author_query and len(author_query) >= 2:
        if author_query:
            items = items.filter(author__name__icontains=author_query)
    if title_query and len(title_query) >= 2:
        if title_query:
            items = items.filter(title__icontains=title_query)

    items = items.order_by(sort_by)
    categories = Category.objects.all()

    cart_product_form = CartNewProductForm()
    return render(request, 'main/index.html', {'items': items,
                                               'categories': categories,
                                               'selected_category': selected_category,
                                               'author_query': author_query,
                                               'min_price': min_price,
                                               'max_price': max_price,
                                               'sort_by': sort_by,
                                               'title_query': title_query,
                                               'cart_product_form': cart_product_form})


def cheap(request):
    items = Book.objects.filter(price__lte=5000)
    return render(request, 'main/index.html', {'items': items})

def detail(request, item_id):
    try:
        item: object = Book.objects.get(id = item_id)
        cart_product_form = CartAddProductForm()
    except:
        return redirect("/")
    return (render(request, 'main/detail.html', {'item':item,
                                                 'cart_product_form': cart_product_form}))

def add_product(request):
    if request.method == "POST":
        Book(title = request.POST.get('title'), price = request.POST.get('price'), description = request.POST.get('description')).save()  
    else:
        pass
    add_form = AddProductForm()
    return render(request, 'main/add.html', {'add_form': add_form})

# @user_passes_test(lambda u: u.is_staff, login_url='/auth/login/')
def create_book(request):
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа, пожалуйста зайдите как Админ.")
    if request.method == 'POST':
        create_form = BookForm(request.POST)
        if create_form.is_valid():
            create_form.save()
            return redirect('main:index')  # Перенаправляем на главную страницу после создания
    else:
        create_form = BookForm()
    return render(request, 'main/create_book.html', {'create_form': create_form})

def view_book(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    return render(request, 'main/view_book.html', {'book': book})

def update_book(request, item_id):
    item = get_object_or_404(Book, pk=item_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа, пожалуйста зайдите как Админ.")
    if request.method == 'POST':
        update_form = BookForm(request.POST, request.FILES, instance=item)
        if update_form.is_valid():
            update_form.save()
            return redirect('main:detail', item_id=item.id)
    else:
        update_form = BookForm(instance=item)
    return render(request, 'main/update_book.html', {'update_form': update_form, 'item': item})

def delete_book(request, item_id):
    item = get_object_or_404(Book, pk=item_id)
    if not request.user.is_staff:
        return HttpResponseForbidden("У вас нет доступа, пожалуйста зайдите как Админ.")
    print(f"Найдена книга с id={item_id}: {item.title}")
    if request.method == 'POST':
        item.delete()
        return redirect('main:index')
    return render(request, 'main/delete_book.html', {'item': item})



