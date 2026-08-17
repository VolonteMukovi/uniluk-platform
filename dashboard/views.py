from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import user_passes_test
from django.views.decorators.http import require_POST
from core.models import (
    Announcement, Article, Faculty, GalleryImage, HeroSlide, Institution,
    PageContent, Registration, Service, SiteSettings, Statistic, StudentGroup,
    Testimonial, CampusBuilding,
)

staff_required = user_passes_test(lambda u: u.is_active and u.is_staff, login_url='/dashboard/login/')


def dashboard_login(request):
    error = None
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user and user.is_staff:
            login(request, user)
            return redirect(request.GET.get('next', '/dashboard/'))
        error = 'Identifiants incorrects ou accès non autorisé.'
    if request.user.is_authenticated and request.user.is_staff:
        return redirect('/dashboard/')
    site = SiteSettings.objects.first()
    return render(request, 'dashboard/login.html', {
        'error': error,
        'site_name': site.name if site else 'UNILUK',
        'site_logo': (site.logo.url if site and site.logo else (site.logo_url if site else '')),
    })


@require_POST
def dashboard_logout(request):
    logout(request)
    return redirect('/dashboard/login/')


@staff_required
def dashboard_index(request):
    counters = {
        'articles': Article.objects.count(),
        'registrations': Registration.objects.count(),
        'faculties': Faculty.objects.count(),
        'media': GalleryImage.objects.count() + HeroSlide.objects.count(),
    }
    return render(request, 'dashboard/index.html', {
        'username': request.user.get_full_name() or request.user.username,
        'counters': counters,
        'site_name': SiteSettings.objects.values_list('name', flat=True).first() or 'UNILUK',
    })
