from django.contrib.auth import authenticate, login as auth_login, logout
from django.shortcuts import redirect, render
from django.contrib import messages
from django.http import JsonResponse
import logging
from .forms import RegisterForm

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
            logger.info(f"User {username} logged in")
            return redirect('home')
        else:
            logger.warning(f"Failed login attempt for {username}")
            messages.error(request, "Неверные учетные данные")

    return redirect('home')

def profile(request):
    return render(request, 'accounts/profile.html')

