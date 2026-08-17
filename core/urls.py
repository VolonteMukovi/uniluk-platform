from django.urls import include, path
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
for prefix, viewset in [
 ('settings',views.SiteSettingsViewSet),('hero-slides',views.HeroSlideViewSet),('statistics',views.StatisticViewSet),
 ('faculties',views.FacultyViewSet),('articles',views.ArticleViewSet),('announcements',views.AnnouncementViewSet),
 ('institutions',views.InstitutionViewSet),('groups',views.StudentGroupViewSet),('buildings',views.CampusBuildingViewSet),
 ('services',views.ServiceViewSet),('gallery',views.GalleryImageViewSet),('testimonials',views.TestimonialViewSet),
 ('pages',views.PageContentViewSet),('registrations',views.RegistrationViewSet)]: router.register(prefix, viewset, basename=prefix)
urlpatterns = [path('', include(router.urls))]
