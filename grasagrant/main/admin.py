from django.contrib import admin
from .models import Category, Type, Fz223, Fz44, Fcp, Grant, Link
# Register your models here.

admin.site.register(Category)
admin.site.register(Type)
admin.site.register(Fz223)
admin.site.register(Fz44)
admin.site.register(Fcp)
admin.site.register(Grant)
admin.site.register(Link)