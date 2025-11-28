from django.shortcuts import render, redirect
from .models import Games, Cart
from django import forms
from django.http import HttpResponse
from django.db.models import Sum, Count


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Games
        fields = ['title', 'price', 'info', 'img']


# Create your views here.
def catalog(request):
    items = Games.objects.all().values()
    cart_count = Cart.objects.count()  # Счёт товаров в корзине
    return render(request, 'index.html', {
        'items': items,
        'cart_count': cart_count
    })

def create_item(request):
    if request.method == 'POST':
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save() # Сохранение информации из формы в базе данных
            return HttpResponse('''
                Статья добавлена в базу данных<br><br>
                <a href="/">Вернуться на главную</a><br><br>
                <a href="/create/">Добавить еще одну статью</a>
            ''')
    form = ArticleForm()
    return render(request, 'form_game.html', {'form': form})

# def add_to_cart(request):
#     if request.method == 'POST':
#         game_id = request.POST.get('game_id')
#         game = Games.objects.get(id=game_id)
#         Cart.objects.create(
#             title=game.title,
#             price=game.price,
#             img=game.img
#         )
#         return HttpResponse(f'''
#             {game.title} в корзинe!<br><br>
#             <a href="/">Вернуться в каталог</a><br>
#             <a href="/cart/">Перейти в корзину</a>
#         ''')


def add_to_cart(request):
    if request.method == 'POST':
        game_id = request.POST.get('game_id')
        game = Games.objects.get(id=game_id)
        Cart.objects.create(
            title=game.title,
            price=game.price,
            img=game.img
        )
        return redirect('/')


def cart_page(request):
    cart_items = Cart.objects.values('title', 'price', 'img').annotate(
        quantity=Count('id'),
        total_price=Sum('price')
    )
    for item in cart_items:
        item['total_price'] = round(item['total_price'], 2)
    total_cart_sum = round(Cart.objects.aggregate(total=Sum('price'))['total'] or 0, 2)
    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'total_cart_sum': total_cart_sum
    })
