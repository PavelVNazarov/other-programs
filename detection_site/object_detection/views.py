from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.shortcuts import redirect
from .models import ImageFeed
#from .object_detection.forms import ImageFeedForm
from django.shortcuts import render
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'object_detection/home.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'object_detection/login.html', {'error': 'Неверные учетные данные'})
    return render(request, 'object_detection/login.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'object_detection/register.html', {'form': form})

@login_required
def dashboard(request):
    images = ImageFeed.objects.filter(user=request.user)
    return render(request, 'object_detection/dashboard.html', {'images': images})

@login_required
def add_image_feed(request):
    if request.method == 'POST':
        form = ImageFeedForm(request.POST, request.FILES)
        if form.is_valid():
            image_feed = form.save(commit=False)
            image_feed.user = request.user  # Привязываем изображение к текущему пользователю
            image_feed.save()
            return redirect('dashboard')  # Перенаправляем на дашборд после успешной загрузки
    else:
        form = ImageFeedForm()
    return render(request, 'object_detection/add_image_feed.html')
    #return render(request, 'object_detection/add_image_feed.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'object_detection/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Неверное имя пользователя или пароль.')
    return render(request, 'object_detection/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')