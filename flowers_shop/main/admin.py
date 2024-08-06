from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StatusDostupa, Tip_Tovara, Kat_Tovara, Tovar, StatusZakaza, Zakaz, BaseOtziv, Otchet, CustomUser
from .models import Otgruzka, Adresa, Zhurnal_status_Zakaza
from orders.models import CartItem
@admin.register(StatusDostupa)
class StatusDostupaAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Status')
    search_fields = ('Status',)

@admin.register(Tip_Tovara)
class Tip_TovaraAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Tip')
    search_fields = ('Tip',)

@admin.register(Kat_Tovara)
class Kat_TovaraAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Kategoriya')
    search_fields = ('Kategoriya',)

@admin.register(Tovar)
class TovarAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Nazvanie', 'Cena', 'Img_url', 'Reiting', 'Opisanie', 'ID_TipTovara', 'ID_KategorTovara')
    search_fields = ('Nazvanie', 'ID_TipTovara__Tip', 'ID_KategorTovara__Kategoriya')
    list_filter = ('ID_TipTovara', 'ID_KategorTovara')

@admin.register(StatusZakaza)
class StatusZakazaAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Status')
    search_fields = ('Status',)

@admin.register(Zakaz)
class ZakazAdmin(admin.ModelAdmin):
    list_display = (
        'ID', 'ID_TipZakaza', 'ID_User', 'ID_adres', 'Kolichestvo_klon', 'Primechanie',
        'DataZakaza', 'Peredano_v_bot', 'Data_sborki', 'Dostavka_nado',
        'Data_peredano_v_dostavku', 'DataDostavki', 'Sobrano', 'Peredano_dostavka',
        'Zakaz_oplachen', 'Zakaz_dostavlen', 'Zakaz_Poluchen', 'Zakaz_zakryt',
        'ID_Status_zakaza'
    )
    search_fields = ('ID_User__username', 'ID_Status_zakaza__Status', 'ID_adres__Nazvanie_adresa', 'Primechanie')
    list_filter = ('ID_Status_zakaza', 'Sobrano', 'Peredano_dostavka', 'Dostavka_nado', 'Peredano_v_bot', 'Zakaz_zakryt', 'Zakaz_oplachen', 'Zakaz_Poluchen')

    def __str__(self):
        return f'Order {self.ID} by {self.ID_User.username}'

@admin.register(BaseOtziv)
class BaseOtzivAdmin(admin.ModelAdmin):
    list_display = ('ID', 'ID_User', 'get_tovar_nazvanie', 'get_otzyv', 'ReitingTovara')
    search_fields = ('ID_User__email', 'ID_Tovara__Nazvanie')
    list_filter = ('ReitingTovara',)

    def get_tovar_nazvanie(self, obj):
        return obj.ID_Tovara.Nazvanie
    get_tovar_nazvanie.short_description = 'Tovar'

    def get_otzyv(self, obj):
        return obj.Otziv
    get_otzyv.short_description = 'Otzyv'

@admin.register(Otchet)
class OtchetAdmin(admin.ModelAdmin):
    list_display = ('ID', 'Data', 'ID_Zakaz', 'Itogo', 'Rashod', 'Dohod', 'Retab')
    search_fields = ('ID_Zakaz__ID', 'Data')
    list_filter = ('Data',)

# Регистрация модели CustomUser в админке
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('StatusID', 'telefon', 'Primechanie', 'tg_Chat_ID', 'tg_User_ID')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('StatusID', 'telefon', 'Primechanie', 'tg_Chat_ID', 'tg_User_ID')}),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'StatusID', 'telefon', 'tg_Chat_ID', 'tg_User_ID')
    search_fields = ('username', 'email', 'first_name', 'last_name', 'StatusID__Status')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups', 'StatusID')

@admin.register(Otgruzka)
class OtgruzkaAdmin(admin.ModelAdmin):
    list_display = ('ID_Zakaz', 'tovar_id', 'quantity', 'cena')
    search_fields = ('ID_Zakaz__id', 'tovar_id__Nazvanie')
    list_filter = ('ID_Zakaz', 'tovar_id')

@admin.register(Adresa)
class AdresaAdmin(admin.ModelAdmin):
    list_display = ('ID_Zakaz', 'ID_User', 'Gorod', 'adres', 'kontakt', 'telefon', 'adres_ediniy', 'Nazvanie_adresa')
    search_fields = ('Gorod', 'adres', 'kontakt', 'telefon', 'Nazvanie_adresa')
    list_filter = ('adres_ediniy', 'Gorod')

@admin.register(Zhurnal_status_Zakaza)
class Zhurnal_status_ZakazaAdmin(admin.ModelAdmin):
    list_display = ('ID', 'ID_Zakaza', 'Izmenenie', 'pole_izm', 'Date', 'peredano')
    search_fields = ('ID_Zakaza__ID', 'Izmenenie')
    list_filter = ('peredano', 'Date')
    ordering = ('-Date',)
    date_hierarchy = 'Date'