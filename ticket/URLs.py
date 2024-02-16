from django.contrib import admin
from django.urls import path
from .views import home, obg, submit, lista_tickets

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('obg/', obg, name='obg'),
    path('submit/', submit, name='submit'),
    path('lista_tickets/', lista_tickets, name='lista_tickets'),
]
