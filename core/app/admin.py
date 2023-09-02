from django.contrib import admin
from django.conf.locale.es import formats as es_formats
from django.contrib.auth.admin import UserAdmin
from django.db import models

from django_google_maps import widgets as map_widgets
from django_google_maps import fields as map_fields

import app.models as model

class HotelFilesInline(admin.StackedInline):    
    model = model.HotelFiles

class HotelBookingInline(admin.StackedInline):    
    model = model.HotelBooking

    fBooking = {"fields": (
        "Account",
        ("iDateBooking","eDateBooking"),
        )}

    fieldsets = (
        ("", fBooking),
        )

class ToursFilesInline(admin.StackedInline):    
    model = model.ToursFiles

class ToursBookingInline(admin.StackedInline):    
    model = model.ToursBooking


class AuthAdminSite(admin.AdminSite):
    index_title = 'Panel Administrativo'
    verbose_name = "MYLIFETRAVEL"

    def get_app_list(self, request, app_label=None):
        """
        Return a sorted list of all the installed apps that have been
        registered in this site. NewMetod for ordering Models
        """
        ordering = {
            "Grupos": 0,
            "Usuarios": 1,
            "Inmuebles": 2,
            "Tours": 3,
            "Noticias": 4,
            "Emails": 5,
            "Links": 6,
            "Configuraciones": 7
            }
        
        app_dict = self._build_app_dict(request, app_label)

        app_list = sorted(app_dict.values(), key=lambda x: x["name"].lower())

        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])

        return app_list


class UserAuthAdmin(UserAdmin):

    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "is_active"
        )

    
    fInformation = {"fields": (
        "first_name",
        "last_name",
        "email",
        "is_active"
        )}
    
    
    fieldsets = (
        ("Informacion", fInformation),
        )

    add_fieldsets = (
        (None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2"),
            },
        ),
    )

    list_filter = ["date_joined"]
    search_fields = ['username']

    es_formats.DATETIME_FORMAT = "d M Y"


class HotelsAdmin(admin.ModelAdmin):

    inlines = [HotelFilesInline]
    #inlines = [HotelFilesInline,HotelBookingInline]
    
    
    list_display = (
        "hCode",
        "hHotel",
        "hLocation",
        "hType",
        "hValue",
        "IsActive"
        )

    fConfig = {"fields": (
        ("hHotel","hCode","IsActive"),
        ("hLocation","hMap"),
        ("hType","hValue"),
        "hBanner"
        )}

    fInfo = {"fields": (
        ("hRooms","hUsers"),
        ("hWifi","hTV","hPool","hGames")
        )}

    fLocation = {"fields": (
        "address",
        "geolocation"
        )}

    fText = {"fields": (
        "hText",
        "hTextX"
        )}

    fieldsets = (
        ("Configuracion", fConfig),
        ("Caracteristicas", fInfo),
        ("Localizacion", fLocation),
        ("Informacion", fText),
        )

    list_filter = ["hLocation","IsActive"]
    search_fields = ['hCode']

    es_formats.DATETIME_FORMAT = "d M Y"
    radio_fields = {'hType': admin.HORIZONTAL}

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }

class ToursAdmin(admin.ModelAdmin):

    inlines = [ToursFilesInline]
    #inlines = [ToursFilesInline,ToursBookingInline]

    list_display = (
        "tCode",
        "tTour",
        "tLocation",
        "tValue"
        )

    fConfig = {"fields": (
        ("tTour","tCode","IsActive"),
        ("tLocation","tMap"),
        ("tDeltaTime","tValue"),
        "tBanner",
        )}

    fInfo = {"fields": (
        ("tHotel","tTransport","tFood","tGuie"),
        )}

    fLocation = {"fields": (
        "address",
        "geolocation"
        )}

    fText = {"fields": (
        "tText",
        "tTextX"
        )}


    fieldsets = (
        ("Configuracion", fConfig),
        ("Caracteristicas", fInfo),
        ("Localizacion", fLocation),
        ("Informacion", fText),
        )

    list_filter = ["tLocation"]
    search_fields = ['tTour']

    es_formats.DATETIME_FORMAT = "d M Y"

    formfield_overrides = {
        map_fields.AddressField: {'widget': map_widgets.GoogleMapsAddressWidget},
    }


class NewsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "nName",
        "nTime",
        "nDate",
        "IsActive"
        )

    fConfig = {"fields": (
        ("nName","IsActive"),
        "nText"
        )}

    fTimes = {"fields": (
        ("nTime","nDate"),
        )}


    fieldsets = (
        ("Configuracion", fConfig),
        ("Fechas", fTimes)
        )

    list_filter = ["nTime","IsActive"]
    search_fields = ['nName']

    es_formats.DATETIME_FORMAT = "d M Y"


class SubscribedEmailsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "eName",
        "eEmail",
        "IsActive"
        )

    fConfig = {"fields": (
        ("eName","eEmail","IsActive"),
        )}

    fieldsets = (
        ("Informacion", fConfig),
        )

    list_filter = ["IsActive"]
    search_fields = ['eName']

    es_formats.DATETIME_FORMAT = "d M Y"


class InformationAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "iTitle",
        "IsActive"
        )

    fConfig = {"fields": (
        ("iTitle","IsActive"),
        "iURL",
        "iText"
        )}

    fieldsets = (
        ("Configuracion", fConfig),
        )

class SettingsAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "sName",
        "sURL",
        "sTel",
        "sEmail"
        )

    fConfig = {"fields": (
        ("sName","IsActive"),
        "sURL",
        ("sIdx","sTel"),
        "sEmail",
        "sAddress"
        )}


    fSocial = {"fields": (
        "sURL1",
        "sURL2",
        "sURL3",
        )}

    fTimes = {"fields": (
        ("sTime1","sTime2"),
        )}

    fMedia = {"fields": (
        "sBackground",
        "sImg1",
        "sImg2",
        "sImg3",
        )}

    fViews = {"fields": (
        ("sHViews","sGViews","sTViews",),
        )}


    fieldsets = (
        ("Configuracion", fConfig),
        ("Social", fSocial),
        ("Horarios Atencion", fTimes),
        #("Imagenes", fMedia),
        ("Vistas", fViews)
        )

##########################################################################
##########################################################################

AdminSite = AuthAdminSite()
admin.site = AdminSite

AdminSite.site_header = "MYLIFETRAVEL"

#admin.site.register(model.Account, UserAuthAdmin)
admin.site.register(model.Hotels, HotelsAdmin)
#admin.site.register(model.News, NewsAdmin)
admin.site.register(model.Tours, ToursAdmin)
#admin.site.register(model.SubscribedEmails, SubscribedEmailsAdmin)
#admin.site.register(model.Information, InformationAdmin)
admin.site.register(model.Settings, SettingsAdmin)

