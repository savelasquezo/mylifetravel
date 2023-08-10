import random

from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.http import JsonResponse
from django.contrib import messages
from django.shortcuts import redirect, render
from django.urls import reverse
from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.auth.views import LoginView

import app.models as model

from .tools import gToken

def CountItems(Type):
    """Count the number of Items in each category Hotels Glammpings Tours
    """
    
    if Type != "t":
        ListItems = model.Hotels.objects.filter(hType=Type)
        Items = ListItems.count() if ListItems else 0
    else:
        ListItems = model.Tours.objects.all()
        Items = ListItems.count() if ListItems else 0

    return Items if Items else random.randint(100,300)

def CountBooking(Type):
    """Count the number of reservations in each category Hotels Glammpings Tours
    """
    
    if Type != "t":
        ListBookin = model.HotelBooking.objects.filter(hHotel__hType=Type)
        nBookin = ListBookin.count() if ListBookin else 0
    else:
        ListTours = model.ToursBooking.objects.all()
        nBookin = ListTours.count() if ListTours else 0

    return nBookin if nBookin else random.randint(100,300)

class IndexView(TemplateView):
    template_name='pages/index.html'

    def get(self, request, *args, **kwargs):

        Settings = model.Settings.objects.filter(IsActive=True).first()
        
        ToursList = model.Tours.objects.filter(IsActive=True) 

        HotelList = model.Hotels.objects.filter(IsActive=True)
        iHotel = HotelList.order_by('-id') if HotelList else []

        Types = ['i','g','t']
        InfoBooking = {}

        for i in Types:
            List1 = CountItems(i)
            List2 = CountBooking(i)
            InfoBooking[i] = [List1, List2]


        context = super().get_context_data(**kwargs)
        context.update({
            'iHotel':iHotel,
            'InfoBooking':InfoBooking,
            'Settings' :Settings,
        })

        return self.render_to_response(context)


class GalleryView(TemplateView):
    template_name='pages/gallery.html'

    
    def get(self, request, *args, **kwargs):

        ITEMS = 3
        
        HotelList = model.Hotels.objects.filter(IsActive=True).order_by('-id')
        iHotel = Paginator(HotelList,ITEMS).get_page(request.GET.get('page')) if HotelList else []
        iTours = model.Tours.objects.filter(IsActive=True).order_by('-id')
        
        ListFix = range(0,(ITEMS - len(HotelList)%ITEMS))
        
        if ListFix == ITEMS and len(HotelList) != 0:
            ListFix = range(0,0)
        
        context = super().get_context_data(**kwargs)
        context.update({
            'iHotel':iHotel,
            'iTours':iTours,
            'ListFix':ListFix
        })
        return self.render_to_response(context)


class GalleryGroupView(TemplateView):
    template_name='pages/gallery.html'

    def get(self, request, *args, **kwargs):

        ITEMS = 3

        Setting = model.Settings.objects.filter(IsActive=True).first()
        rType = self.kwargs.get('hType')
        iTitle = "Catalogo"

        context = super().get_context_data(**kwargs)

        if rType == 't':
            iTours = model.Tours.objects.filter(IsActive=True).order_by('id')
            iTitle = model.Tours._meta.verbose_name

            Setting.sTViews += 1
            Setting.save()

            context.update({'iTours':iTours,})
        
        if rType != 't':
            HotelList = model.Hotels.objects.filter(hType=rType, IsActive=True).order_by('id')
            iHotel = Paginator(HotelList,ITEMS).get_page(request.GET.get('page')) if HotelList else []
            iTitle = HotelList.first().get_hType_display() if HotelList else []

            if rType == 'h':
                Setting.sHViews += 1
                Setting.save()

            if rType == 'g':
                Setting.sGViews += 1
                Setting.save()
        
            context.update({'iHotel':iHotel})
            
        context.update({'iTitle':f"{iTitle}s"})
        return self.render_to_response(context)

class InfoHotelView(TemplateView):
    template_name='pages/info.html'
    
    def get(self, request, *args, **kwargs):

        rCode = self.kwargs.get('hCode')
        hHotel = model.Hotels.objects.get(hCode=rCode)
        
        if hHotel:
            fHotel = model.HotelFiles.objects.filter(hHotel__hCode=rCode)
        
        hType = hHotel.get_hType_display()
        
        context = super().get_context_data(**kwargs)
        context.update({
            'hType':hType,
            'fHotel': fHotel,
            'hHotel': hHotel,
        })
        return self.render_to_response(context)

class InfoToursView(TemplateView):
    template_name='pages/info.html'

    
    def get(self, request, *args, **kwargs):

        rCode = self.kwargs.get('tCode')
        if model.Tours.objects.get(tCode=rCode):
            fTours = model.ToursFiles.objects.filter(tTour__tCode=rCode)
            iTours = fTours.first()

        context = super().get_context_data(**kwargs)
        context.update({
            'fTours': fTours,
            'iTours': iTours,
        })
        return self.render_to_response(context)


class BookingView(TemplateView):
    template_name='pages/booking.html'

    def get(self, request, *args, **kwargs):

        ITEMS = 5
        MAXPAGES = 5

        BookingList = model.HotelBooking.objects.filter(Account=request.user).order_by("id")[:ITEMS*MAXPAGES]
        iListBooking = Paginator(BookingList,ITEMS).get_page(request.GET.get('page'))

        iFileFix = ITEMS - len(BookingList)%ITEMS

        if iFileFix == ITEMS and len(BookingList) != 0:
            iFileFix = 0

        context = super().get_context_data(**kwargs)
        context.update({
            "BookingList": BookingList,
            'iListBooking':iListBooking,
            'FixListPage':range(0,iFileFix)
        })

        return self.render_to_response(context)

class AuthLoginView(UserPassesTestMixin, LoginView):
    template_name='registration/login.html'

    def test_func(self):
        """ UserAutenticate Cant Create NewUser, When User is Antenticate test_func is False
        """
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        """When test_fun(self) is False, Redirect User Autenticate to Home
        """
        return redirect(reverse('index'))


    def form_invalid(self, form):
        messages.error(self.request, 'Usuario/Contraseña Incorrectos', extra_tags="title")
        messages.error(self.request, 'Intentelo Nuevamente', extra_tags="info")
        return super().form_invalid(form)

class AuthSingupView(UserPassesTestMixin, TemplateView):
    template_name='registration/singup.html'

    def test_func(self):
        """ UserAutenticate Cant Create NewUser, When User is Antenticate test_func is False
        """
        return not self.request.user.is_authenticated

    def handle_no_permission(self):
        """When test_fun(self) is False, Redirect User Autenticate to Home
        """
        return redirect(reverse('Index'))

    def post(self, request, *args, **kwargs):

        username = request.POST['username']
        password = request.POST['password']
        full_name = request.POST['full_name']
        email = request.POST['email']

        if not re.match(r'^[a-zA-Z0-9]+$', username):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, 'El Nombre de Usuario no es Valido', extra_tags="info") 
            return redirect(reverse('singup'))

        if model.Users.objects.filter(username=username):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, 'El Nombre de Usuario no esta Disponible', extra_tags="info") 
            return redirect(reverse('singup'))

        if model.Users.objects.filter(email=email, is_active=True):
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, 'El Email no esta Disponible', extra_tags="info") 
            return redirect(reverse('singup'))
        
        request.session['django_messages'] = []

        try:
            nUser = model.Users.objects.create(
                username = username,
                full_name = full_name,
                email = email
            )
            
            nUser.set_password(password)
            nUser.save()

            messages.success(request, '¡Registro Exitoso!', extra_tags="title")
            messages.success(request, '¡Ahora eres miembro de MylifeTravel!', extra_tags="info")
            return redirect(reverse('login'))

        except Exception as e:
            messages.error(request, '¡Registro Incompleto!', extra_tags="title")
            messages.error(request, 'Ha ocurrido un error durante el registro', extra_tags="info")
            return redirect(reverse('singup'))  


######################################################################
######################################################################
######################################################################


def ComingSoonView(request):
    return render(request, '000.html')


def AddSubscribedEmail(request):
  if request.method == 'POST':
    iName = request.POST.get('name')
    iEmail = request.POST.get('email')

    my_model = model.SubscribedEmails(eName=iName, eEmail=iEmail)
    my_model.save()

    return JsonResponse({'success': True})
  else:
    return JsonResponse({'success': False})