from django.db import models

from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from django_google_maps import fields as map_fields

lst_sts = (('g','Glamping'),('i','Inmueble'))

def CustomUploadToHotel(instance, filename):
    return f"media/hotel/{instance.hHotel.hHotel}/{filename}"

def CustomUploadToTours(instance, filename):
    return f"media/tours/{instance.tTour.tTour}/{filename}"

class Account(AbstractUser):

    class Meta:
        verbose_name = _("Usuario")
        verbose_name_plural = _("Usuarios")

####################################################################################################################
####################################################################################################################
####################################################################################################################

class Hotels(models.Model):

    hCode = models.CharField(_("Codigo"), max_length=32, unique=False)
    
    hHotel = models.CharField(_("Nombre"), max_length=64, blank=False, null=False)
    hLocation = models.CharField(_("Ciudad"), max_length=64, blank=False, null=False)

    hMap = models.URLField(_("MAP"), max_length=512, blank=True, null=True, default="https://www.google.com/maps/search/",
        help_text="URL Ubicacion del Inmueble https://www.google.com/maps/search/?api=1&query=40.712776,-74.005974")

    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    hType = models.CharField(_("Caracteristica"),choices=lst_sts, max_length=64)
    hValue = models.IntegerField(_("Valor"),blank=True, null=True, default=0,
        help_text="Valor de Estadia Dia/Noche ($COP)")

    hBanner = models.ImageField(_("Miniatura"), height_field=None, width_field=None, max_length=64,
        upload_to="media/index/banner/hotel", help_text="720px-Width 600px-Height")
    
    hText = models.TextField(_("Texto"),blank=True, null=True, max_length=512,
        help_text="Descripcion Resumida del Inmueble")
    
    hTextX = models.TextField(_("Texto"),blank=True, null=True, max_length=1024,
        help_text="Descripcion Completa del Inmueble")

    hRooms = models.SmallIntegerField(_("Habitaciones"),blank=True, null=True, default=1)
    hUsers = models.SmallIntegerField(_("Capacidad"),blank=True, null=True, default=1)

    hWifi = models.CharField(_("Wifi"), blank=True, null=True, max_length=64, help_text="Ejemplo: 200M")
    hTV = models.CharField(_("TV"), blank=True, null=True, max_length=64, help_text="Ejemplo: Smart4K 60'")
    hPool =  models.CharField(_("Zonas Humedas"), blank=True, max_length=64, null=True, help_text="Ejemplo: Olímpica/Jacuzzi")
    hGames = models.CharField(_("Juegos"), blank=True, null=True, max_length=64, help_text="Ejemplo: Futbol/Basquetball")

    IsActive = models.BooleanField(_("¿Activo?"), default=True)

    def __str__(self):
        return f"Inmueble: {self.hHotel}"

    class Meta: 
        verbose_name = _("Inmueble")
        verbose_name_plural = _("Inmuebles")

class HotelFiles(models.Model):
    hHotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    hFiles = models.ImageField(_("Imagenes"), upload_to=CustomUploadToHotel, height_field=None, width_field=None, max_length=64,
        help_text="Ancho[640px]-Alto[480px]")


    def __str__(self):
        return "Imagen/Archivo"
    
    class Meta:
        verbose_name = _("Foto")
        verbose_name_plural = _("Galeria")


class HotelBooking(models.Model):
    hHotel = models.ForeignKey(Hotels, on_delete=models.CASCADE)
    Account = models.ForeignKey(Account, on_delete=models.CASCADE)
    iDateBooking = models.DateField(_("Inicia"),auto_now=False,auto_now_add=False)
    eDateBooking = models.DateField(_("Finaliza"),auto_now=False,auto_now_add=False)

    def __str__(self):
        return "Ticket"
    
    class Meta:
        verbose_name = _("Reservacion")
        verbose_name_plural = _("Reservaciones")

####################################################################################################################
####################################################################################################################
####################################################################################################################

class Tours(models.Model):
    
    tCode = models.CharField(_("Codigo"), max_length=32, unique=False)

    tTour = models.CharField(_("Nombre"), max_length=64, blank=False, null=False)
    tLocation = models.CharField(_("Destino"), max_length=64, blank=False, null=False)
    tMap = models.URLField(_("MAP"), max_length=512, blank=True, null=True, default="https://www.google.com/maps/search/",
        help_text="URL Ubicacion del Tour https://www.google.com/maps/search/?api=1&query=40.712776,-74.005974")

    address = map_fields.AddressField(max_length=200)
    geolocation = map_fields.GeoLocationField(max_length=100)

    tBanner = models.ImageField(_("Miniatura"), height_field=None, width_field=None, max_length=64,
        upload_to="media/index/banner/tours", help_text="300px-Width 300px-Height")

    tValue = models.IntegerField(_("Valor"),blank=True, null=True, default=0)
    tAmmount = models.IntegerField(_("Cupos"),blank=True, null=True, default=0)


    tText = models.TextField(_("Texto"),blank=True, null=True, max_length=512,
        help_text="Descripcion Resumida del Tour")
    
    tTextX = models.TextField(_("Texto"),blank=True, null=True, max_length=1024,
        help_text="Descripcion Completa del Tour")

    tDeltaTime = models.SmallIntegerField(_("Duracion"),blank=True, null=True, default=1,
        help_text="Duracion del Recorrido (Dias)")
    
    tHotel = models.CharField(_("Alojamiento"), blank=True, null=True, max_length=64, help_text="Hostal")
    tTransport = models.CharField(_("Transporte"), blank=True, null=True, max_length=64, help_text="Bus Emperador")
    tFood = models.CharField(_("Alimentacion"), blank=True, null=True, max_length=64, help_text="Desayuno/Refrigerio")
    tGuie = models.CharField(_("Guia"), blank=True, null=True, max_length=64, help_text="Tour Guiado")

    IsActive = models.BooleanField(_("¿Activo?"), default=True)

    def __str__(self):
        return f"Tour: {self.tTour}"

    class Meta:
        verbose_name = _("Tour")
        verbose_name_plural = _("Tours")


class ToursFiles(models.Model):
    
    tTour = models.ForeignKey(Tours, on_delete=models.CASCADE)
    
    tFiles = models.ImageField(_("Imagenes"), upload_to=CustomUploadToTours, height_field=None, width_field=None, max_length=64,
        help_text="Ancho[640px]-Alto[480px]")


    def __str__(self):
        return "Imagen/Archivo"
    
    class Meta:
        verbose_name = _("Foto")
        verbose_name_plural = _("Galeria")


class ToursBooking(models.Model):
    tTour = models.ForeignKey(Tours, on_delete=models.CASCADE)
    tAccount = models.ForeignKey(Account,verbose_name="Usuario",on_delete=models.CASCADE)

    def __str__(self):
        return "Ticket"
    
    class Meta:
        verbose_name = _("Reservacion")
        verbose_name_plural = _("Reservaciones")

####################################################################################################################
####################################################################################################################
####################################################################################################################


class News(models.Model):

    nName = models.CharField(_("Titular"), max_length=64, blank=False, null=False)
    
    nTime = models.DateField(_("Fecha Publicacion"), auto_now=False, auto_now_add=False, default=timezone.now)
    nDate = models.CharField(_("Fecha Evento"), max_length=64, blank=False, null=False, 
        help_text="Fecha Visualizada-Texto")
    
    nText = models.TextField(_("Informacion"), max_length=128, blank=False, null=False, 
        help_text="Texto Max-128")
    
    IsActive = models.BooleanField(_("¿Activo?"), default=True)

    def __str__(self):
        return f"Noticia: #{self.id}"

    class Meta:
        verbose_name = _("Noticia")
        verbose_name_plural = _("Noticias")

class SubscribedEmails(models.Model):

    eName = models.CharField(_("Nombre"), max_length=64, blank=False, null=False)
    eEmail = models.EmailField(_("Email"), unique=True, blank=False, null=False, max_length=254)
    
    IsActive = models.BooleanField(_("Subscrito/Activo"), default=True)

    def __str__(self):
        return f"Email: {self.eEmail}"

    class Meta:
        verbose_name = _("Email")
        verbose_name_plural = _("Emails")

class Information(models.Model):

    iTitle = models.CharField(_("Titulo"), max_length=64, blank=False, null=False,
        help_text="Titulo/Encabezado")
    
    iURL = models.CharField(_("URL"), max_length=32, blank=False, null=False, 
        help_text="Local/Ref (SinEspacios-OnlyURL)")
    
    iText = models.TextField(_("Texto"))
    
    IsActive = models.BooleanField(_("¿Activo?"), default=True)

    def __str__(self):
        return f"Informacion: {self.iTitle}"

    class Meta:
        verbose_name = _("Link")
        verbose_name_plural = _("Links")

class Settings(models.Model):

    sName = models.CharField(_("Configuracion"), max_length=64, blank=False, null=False, help_text="Organizacion/Empresa")
    sURL = models.URLField(_("URL"), max_length=128, blank=True, null=True)

    sIdx = models.SmallIntegerField(_("Indicativo"), blank=True, null=True, default=57)    
    sTel = models.CharField(_("Telefono"), max_length=64, blank=True, null=True)
    
    sEmail = models.EmailField(_("Correo"), max_length=254, blank=True, null=True)
    
    sTime1 = models.TimeField(_("Inicia"), auto_now=False, auto_now_add=False)
    
    sTime2 = models.TimeField(_("Finaliza"), auto_now=False, auto_now_add=False)

    sAddress = models.CharField(_("Address"), max_length=64, blank=True, null=True)
    
    sURL1 = models.URLField(_("Instagram"), max_length=128, blank=True, null=True, 
        help_text="https://www.instagram.com/")
    sURL2 = models.URLField(_("Facebook"), max_length=128, blank=True, null=True, 
        help_text="https://www.facebook.com/")
    sURL3 = models.URLField(_("Twitter"), max_length=128, blank=True, null=True, 
        help_text="https://twitter.com/")

    sBackground = models.ImageField(_("Background"), upload_to="media/index/settings/", height_field=None, width_field=None, max_length=64, blank=True, null=True,
        help_text="1200px-Width 800px-Height")

    sImg1 = models.ImageField(_("Turismo"), upload_to="media/index/settings/", height_field=None, width_field=None, max_length=64, blank=True, null=True,
        help_text="360px-Width 280px-Height")

    sImg2 = models.ImageField(_("Hoteles"), upload_to="media/index/settings/", height_field=None, width_field=None, max_length=64, blank=True, null=True,
        help_text="360px-Width 280px-Height")

    sImg3 = models.ImageField(_("Glampings"), upload_to="media/index/settings/", height_field=None, width_field=None, max_length=64, blank=True, null=True,
        help_text="360px-Width 280px-Height")

    sHViews = models.BigIntegerField(null=True,blank=True)
    sGViews = models.BigIntegerField(null=True,blank=True)
    sTViews = models.BigIntegerField(null=True,blank=True)

    IsActive = models.BooleanField(_("¿Activo?"), default=True, unique=True)

    def __str__(self):
        return f"Configuracion: {self.sName}"

    class Meta:
        verbose_name = _("Configuracion")
        verbose_name_plural = _("Configuraciones")