from django.contrib import admin

from .models import Company, Recruit, Application

# Register your models here.


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    pass


@admin.register(Recruit)
class RecuritAdmin(admin.ModelAdmin):
    pass


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    pass
