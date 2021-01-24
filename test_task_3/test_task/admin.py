from django.contrib import admin

from .models import Booking, Table, Visitor

# Register your models here.

admin.site.register(Table)
admin.site.register(Booking)
admin.site.register(Visitor)