from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import StatusDostupa, Tip_Tovara, Kat_Tovara, Tovar, StatusZakaza, Zakaz, BaseOtziv, Otchet, CustomUser

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
    list_display = ('ID', 'ID_TipZakaza', 'ID_User', 'get_tovar_nazvanie', 'Kolichestvo', 'DataZakaza', 'DataDostavki', 'Polucheno', 'ID_Status')
    search_fields = ('ID_User__email', 'ID_Tovara__Nazvanie')
    list_filter = ('ID_Status', 'Polucheno')

    def get_tovar_nazvanie(self, obj):
        return obj.ID_Tovara.Nazvanie
    get_tovar_nazvanie.short_description = 'Tovar'

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
