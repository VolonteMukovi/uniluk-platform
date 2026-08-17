from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie
from django.urls import path
@ensure_csrf_cookie
def index(request): return render(request, 'index.html')
urlpatterns = [path('', index, name='home')]
