from django.contrib import admin
from django.contrib.auth.models import BaseUserManager

from .models import *

admin.site.register(Event)
admin.site.register(Field)


class HomePageSection(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not HomePage.objects.exists()

    def has_change_permission(self, request, obj=None):
        return HomePage.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['first_name','last_name','username', 'email']  # ستون‌هایی که می‌خواهید نمایش داده شوند
    search_fields = ['first_name','last_name','username', 'email']  # فیلدهای جستجو

admin.site.register(HomePage, HomePageSection)
admin.site.register(Slide)
admin.site.register(Information)
admin.site.register(Supporter)
admin.site.register(League)
admin.site.register(Alert)
admin.site.register(StudentDashboard)
admin.site.register(Commment)
admin.site.register(ContactUsForm)
