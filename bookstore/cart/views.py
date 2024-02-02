from django.shortcuts import render, get_object_or_404, redirect
from django.views.decorators.http import require_POST
from .cart import Cart
from .forms import CartAddProductForm
from main.models import Book
from django.http import JsonResponse
from .models import ClientLocation
from django.views.decorators.csrf import csrf_exempt
from cloudipsp import Api, Checkout
import json
# Create your views here.

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    form = CartAddProductForm(request.POST)
    if form.is_valid():
        cd = form.cleaned_data
        if cd['quantity'] == 0:
            cart.remove(product)
        else:
            cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'])
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Book, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    for item in cart:
        item['update_quantity_form'] = CartAddProductForm(initial={'quantuty': item['quantity'], 'update': True})
    return render(request, 'cart/detail.html', {'cart': cart})


def buy_fondy(request):
    cart = Cart(request)
    total = int(cart.get_total_price())
    api = Api(merchant_id=1396424,
                secret_key='test')
    checkout = Checkout(api=api)
    data = {
            "currency": "KZT",
            "amount": str(total)+'00'
        }
    url = checkout.url(data).get('checkout_url')
    return redirect(url)

def geolocations(request):
    print("geolocations")
    if request.method == 'POST':
        latitude = request.POST.get('latitude')
        longitude = request.POST.get('longitude')
        print("lat:", latitude)
        print("long:", longitude)

        # Создание записи о местоположении клиента в базе данных
        client_location = ClientLocation.objects.create(latitude=latitude, longitude=longitude)
        print("clinet:", client_location)
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

def show_client_location(request):
    # Получение последнего сохраненного местоположения клиента из базы данных
    latest_location = ClientLocation.objects.last()
    print("show:", latest_location)
    # Передача данных в шаблон
    context = {
        'latitude': latest_location.latitude if latest_location else None,
        'longitude': latest_location.longitude if latest_location else None,
    }
    print("context:", context)
    return render(request, 'cart/geolocations.html', context)

@csrf_exempt
def save_location(request):
    print("save:")
    if request.method == 'POST':
        try:
            # Получение данных о местоположении из запроса
            data = json.loads(request.body)
            print("data:", data)
            latitude = data.get('latitude')
            longitude = data.get('longitude')
            print("lat:", latitude)
            print("long:", longitude)
            # latitude = data.get(43.2504832)
            # longitude = data.get(76.8835584)

            # Далее можно сохранить эти данные в базе данных или выполнить другие действия

            return JsonResponse({'status': 'success', 'message': 'Location saved successfully'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})

    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})


# stripe.api_key = settings.STRIPE_SECRET_KEY

# def checkout(request):
#     if request.method == 'POST':
#         token = request.POST.get('stripeToken')
#         try:
#             charge = stripe.Charge.create(
#                 amount=1000,  # сумма в центах
#                 currency='usd',
#                 description='Заказ книги',  # описание платежа
#                 source=token,
#             )
#             # Ваш код обработки успешного платежа
#             return render(request, 'cart/checkout_success.html')
#         except stripe.error.CardError as e:
#             # Обработка ошибки, связанной с картой
#             return render(request, 'cart/checkout_failure.html', {'error_message': str(e)})

#     return render(request, 'cart/checkout.html')

# def checkout(request):
#     print("1")
#     if request.method == 'POST':
#         print("Equal POST1")
#         intent = stripe.PaymentIntent.create(
#             amount=2000,  # сумма в центах
#             currency='usd',
#             description='Заказ книги',  # описание платежа
#             payment_method=request.POST.get('payment_method'),
#             confirm=True,
#         )
#         print("intent create")
#         return render(request, 'cart/checkout_success.html')
    
#     # Добавьте свою логику для GET-запроса, если необходимо
#     print("checkout.html")
#     return render(request, 'cart/checkout.html')

# @csrf_exempt
# def create_payment_intent(request):
#     print("2")
#     if request.method == 'POST':
#         print("equal 2")
#         try:
#             intent = stripe.PaymentIntent.create(
#                 amount=1000,  # сумма в центах
#                 currency='usd',
#                 description='Заказ книги',  # описание платежа
#             )
#             return JsonResponse({'client_secret': intent.client_secret})
#         except stripe.error.CardError as e:
#             return JsonResponse({'error': str(e)}, status=403)

#     return HttpResponse(status=400)
  
# def create_payment_intent(request):
#     if request.method == 'POST':
#         print("equal 2")
#         try:
#             intent = stripe.PaymentIntent.create(
#                 amount=1000,  # сумма в центах
#                 currency='usd',
#                 description='Заказ книги',  # описание платежа
#             )
#             return JsonResponse({'client_secret': intent.client_secret})
#         except stripe.error.CardError as e:
#             return JsonResponse({'error': str(e)}, status=403)
        


#     # Возвращаем JsonResponse с информацией о PaymentIntent
#     return JsonResponse({'client_secret': intent.client_secret})

