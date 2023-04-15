import random

from django.views.generic.base import TemplateView
from django.core.paginator import Paginator
from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Count

import app.models as model

from .tools import gToken

def CountBooking(hT):
    
    if hT != "Tours":
        ListBookin = model.HotelBooking.objects.filter(hHotel__hType=hT)
        nBookin = ListBookin.annotate(i=Count('id')).values_list('i',flat=True).first() if ListBookin else 0
    else:
        ListTours = model.ToursBooking.objects.filter()
        nBookin = ListTours.annotate(i=Count('id')).values_list('i',flat=True).first() if ListTours else 0

    return nBookin if nBookin else random.randint(100,300)

class IndexView(TemplateView):
    template_name='app/index.html'

    def get(self, request, *args, **kwargs):

        Info = model.Information.objects.filter(IsActive=True)
        
        ToursList = model.Tours.objects.filter(IsActive=True) 
        iTours = ToursList.order_by("id")[:9] if ToursList else []

        HotelList = model.Hotels.objects.filter(IsActive=True)
        iHotel = HotelList.order_by('id')[:3] if HotelList else []

        ListNews = model.News.objects.filter(IsActive=True)[:2]
        ListBooking = [CountBooking(i) for i in ['Hoteleria', 'Inmuebles', 'Glampings', 'Tours']]

        context = super().get_context_data(**kwargs)
        context.update({
            "Info":Info,
            'iHotel':iHotel,
            'iTours':iTours,
            'ListNews':ListNews,
            'ListBooking':ListBooking
        })

        return self.render_to_response(context)


class GalleryView(TemplateView):
    template_name='app/pages/gallery.html'

    
    def get(self, request, *args, **kwargs):

        ITEMS = 6
        
        HotelList = model.Hotels.objects.all().order_by('id')
        iHotel = Paginator(HotelList,ITEMS).get_page(request.GET.get('page')) if HotelList else []
        
        iHotelFix = range(0,(ITEMS - len(HotelList)%ITEMS))
        
        if iHotelFix == ITEMS and len(HotelList) != 0:
            iHotelFix = range(0,0)
        
        context = super().get_context_data(**kwargs)
        context.update({
            'iHotel':iHotel,
            'iHotelFix':iHotelFix
        })
        return self.render_to_response(context)


class GalleryGroupView(TemplateView):
    template_name='app/pages/gallery.html'

    def get(self, request, *args, **kwargs):

        ITEMS = 6
        
        rType = self.kwargs.get('hType')

        if rType == 't':
            iTitle = model.Tours._meta.verbose_name

        HotelList = model.Hotels.objects.filter(hType=rType).order_by('id') if rType != 't' else model.Tours.objects.all().order_by('id')
        iHotel = Paginator(HotelList,ITEMS).get_page(request.GET.get('page')) if HotelList else []
        
        iHotelFix = range(0,(ITEMS - len(HotelList)%ITEMS)) if HotelList else 0
        
        if rType != 't':
            iTitle = HotelList.first().get_hType_display() if HotelList else []
        
        if iHotelFix == ITEMS and len(HotelList) != 0:
            iHotelFix = range(0,0)
        
        context = super().get_context_data(**kwargs)
        context.update({
            'iTitle':iTitle,
            'iHotel':iHotel,
            'iHotelFix':iHotelFix
        })
        return self.render_to_response(context)

class InfoHotelView(TemplateView):
    template_name='app/pages/info.html'

    
    def get(self, request, *args, **kwargs):

        rCode = self.kwargs.get('hCode')
        hHotel = model.Hotels.objects.get(hCode=rCode)
        
        if hHotel:
            fHotel = model.HotelFiles.objects.filter(hHotel__hCode=rCode)
            iHotel = fHotel.first()  
        
        hType = hHotel.get_hType_display()
        
        context = super().get_context_data(**kwargs)
        context.update({
            'hType':hType,
            'fHotel': fHotel,
            'iHotel': iHotel,
        })
        return self.render_to_response(context)

class InfoToursView(TemplateView):
    template_name='app/pages/info.html'

    
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


class LegalView(TemplateView):
    template_name='app/pages/legal.html'

    
    def get(self, request, *args, **kwargs):

        rURL = self.kwargs.get('iURL')
        InfoLink = model.Information.objects.get(iURL=rURL)
        

        context = super().get_context_data(**kwargs)
        context.update({
            'InfoLink': InfoLink,
        })
        return self.render_to_response(context)



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