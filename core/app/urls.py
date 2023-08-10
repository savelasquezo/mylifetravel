from django.contrib.auth import views as auth_views
from django.urls import path

import app.views as views

urlpatterns = [

    path('', views.IndexView.as_view(), name='index'),

    path('@', views.ComingSoonView, name='ComingSoon'),
    path('AddEmail', views.AddSubscribedEmail, name='AddEmail'),

    path('accounts/singup',views.AuthSingupView.as_view(), name='singup'),
    path('accounts/login',views.AuthLoginView.as_view(), name='login'),
    path('accounts/logout', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/booking',views.BookingView.as_view(), name='booking'),

    path('gallery', views.GalleryView.as_view(), name='gallery'),
    path('gallery/<str:hType>', views.GalleryGroupView.as_view(), name='gallery-group'),
    path('gallery/h/<int:hCode>', views.InfoHotelView.as_view(), name='info-hotel'),
    path('gallery/t/<int:tCode>', views.InfoToursView.as_view(), name='info-tours'),
    
] 
