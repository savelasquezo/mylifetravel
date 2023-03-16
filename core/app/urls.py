from django.contrib.auth import views as auth_views
from django.urls import path, include

import app.views as views

urlpatterns = [
    #path("accounts/", include("django.contrib.auth.urls")),

    path('', views.IndexView.as_view(), name='index'),

    path('@', views.ComingSoonView, name='ComingSoon'),
    path('AddEmail', views.AddSubscribedEmail, name='AddEmail'),
    
    path('gallery', views.GalleryView.as_view(), name='gallery'),
    path('gallery/<str:hType>', views.GalleryGroupView.as_view(), name='gallery-group'),
    
    path('gallery/h/<int:hCode>', views.InfoHotelView.as_view(), name='info-hotel'),
    path('gallery/t/<int:tCode>', views.InfoToursView.as_view(), name='info-tours'),
    path('legal/<str:iURL>', views.LegalView.as_view(), name='legal'),
    
] 
