from tkinter.font import names

from Main.views import *
from Zarinpal.views import *
from user.views import *
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('sign-up/', sign_up, name='signup'),
    path("zarinpal/", include('Zarinpal.urls')),
    path('login-student/', login_student, name='login_student'),
    path('student-dashboard/', dashboard_student, name='dashboard_student'),
    path('profile-setting/', profile_setting, name='profile_setting'),
    path('about-us/' , about_us, name='about_us'),
    path('contact-us/', contact_view , name='contact_us'),
    path('doucument/' , doucument, name='doucument'),
    path('developers/' , developers, name='developers'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
