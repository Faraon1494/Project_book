from decimal import Decimal
from django.conf import settings
from main.models import Book

class Cart(object):
    def __init__(self, request):
        """
        Инициализация корзины
        :param request:
        """
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # сохраняем пустую корзину в сессию
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart

    def __iter__(self):
        """
        Перебираем товары в корзине и получаем тоавры из базы данных
        :return: генератор товаров
        """
        product_ids = self.cart.keys()
        # Получаем товары и добавляем их в корзину
        products = Book.objects.filter(id__in = product_ids)

        cart = self.cart.copy()
        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self) -> int:
        """
        Считаем сколько товаров в корзине
        :reutrn: int
        """
        return sum(item['quantity'] for item in self.cart.values())
    
    def add(self, product, quantity = 1, update_quantity = False):
        """
        Добавление тоавара в корзину
        :param product:
        :param quantity:
        :param update_quantity:
        :return:
        """
        product_id = str(product.id)
        if product_id not in self.cart:
            # Если изначально товара не было в корзине
            self.cart[product_id] = {'quantity': 0,
                                     'price': str(product.price)}
        if update_quantity:
            self.cart[product_id]['quantity'] = quantity
        else:
            self.cart[product_id]['quantity'] += quantity
        self.save()

    def save(self):
            self.session.modified = True

    def remove(self, product):
        """"
        Удаляем товара
        :param product:
        :return:
        """
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def get_total_price(self):
        """
        получение общий стоимости покупок
        :return int:
        """
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values()) 
    
    def clear(self):
        """
        Очищение корзины в сессии
        """
        del self.session[settings.CART_SESSION_ID]
        self.save()
        

