from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
import logging
from .forms import RegisterForm, ProfileForm
from cart.models import Cart, CartItem
from .models import CustomUser

logger = logging.getLogger(__name__)

def custom_logout(request):
    logout(request)
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = True
                user.save()
                auth_login(request, user)
                logger.info(f"User {user.username} successfully registered")
                return JsonResponse({'success': True})
            except Exception as e:
                logger.error(f"Error during user registration: {str(e)}")
                return JsonResponse({'success': False, 'errors': {'form': 'Ошибка при сохранении пользователя'}})
        else:
            logger.warning(f"Form validation errors: {form.errors}")
            errors = {}
            for field, error_list in form.errors.items():
                errors[field] = error_list[0]
            return JsonResponse({'success': False, 'errors': errors})
    else:
        form = RegisterForm()
        return JsonResponse({
            'form': form.as_p(),
            'csrf_token': str(request.COOKIES.get('csrftoken', ''))
        })


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            auth_login(request, user)

            # Перенос корзины, если пользователь не админ
            if not user.is_staff:
                session_key = request.session.session_key
                if not session_key:
                    request.session.create()
                    session_key = request.session.session_key

                session_cart = Cart.objects.filter(session_key=session_key, user__isnull=True).first()

                if session_cart:
                    existing_cart = Cart.objects.filter(user=user).first()

                    if existing_cart:
                        # Объединяем корзины
                        for item in session_cart.cartitem_set.all():
                            main_item, created = CartItem.objects.get_or_create(cart=existing_cart, dishes=item.dishes)
                            main_item.quantity += item.quantity
                            main_item.save()
                        session_cart.delete()
                    else:
                        # Просто привязываем корзину к пользователю
                        session_cart.user = user
                        session_cart.save()

                return redirect('home')

            else:
                return redirect('/admin')  # Если админ

    return redirect('home')  # Если не прошла аутентификация



def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)  # Обрабатываем файлы (например, аватар)
        if form.is_valid():
            form.save()  # Сохраняем данные формы
            return redirect('accounts:profile')  # Перенаправляем на страницу профиля после сохранения
    else:
        form = ProfileForm(instance=request.user)  # Загружаем текущие данные пользователя

    return render(request, 'accounts/profile.html', {'form': form})

