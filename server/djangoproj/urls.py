from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView


urlpatterns = [
    path(
        'admin/',
        admin.site.urls,
    ),
    path(
        'about/',
        TemplateView.as_view(template_name='About.html'),
        name='about',
    ),
    path(
        'contact/',
        TemplateView.as_view(template_name='Contact.html'),
        name='contact',
    ),
    path(
        'djangoapp/',
        include('djangoapp.urls'),
    ),
    path(
        '',
        TemplateView.as_view(template_name='Home.html'),
        name='home',
    ),
    path(
        'login/',
        TemplateView.as_view(template_name='index.html'),
        name='login',
    ),
    path(
        'register/',
        TemplateView.as_view(template_name='index.html'),
        name='register',
    ),
    path(
        'dealers/',
        TemplateView.as_view(template_name='index.html'),
        name='dealers',
    ),
    path(
        'dealer/<int:dealer_id>',
        TemplateView.as_view(template_name='index.html'),
        name='dealer',
    ),
    path(
        'postreview/<int:dealer_id>',
        TemplateView.as_view(template_name='index.html'),
        name='postreview',
    ),
] + static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT,
)
