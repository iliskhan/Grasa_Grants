from main.models import Type, Grant, Fcp, Fz44, Fz223, Category, Region

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers

# Create your views here.
global_variables = globals()

def index(request):
    return redirect('types_list', tab_name='Grant')

class TypesList(View):

    def get(self, request, tab_name):
        category = Category.objects.get(tab_name=tab_name)
        types = Type.objects.filter(category=category)
        
        return render(
            request, 
            'types_list.html',
            context = {'types': types, 'tab_name': tab_name},
        )

def detailed(request, tab_name, pk):
    data = get_object_or_404(global_variables[tab_name], id=pk)
    return render(
        request,
        f'{tab_name.lower()}.html',
        context = {'data': data},
    )

def subtypes_list(request, tab_name, pk):
    subtype_name = f"{tab_name.lower()}_name"
    kwargs = {subtype_name: pk}
    subtypes = global_variables[tab_name].objects.filter(**kwargs)

    return render(
        request,
        f'{tab_name.lower()}_list.html',
        context={f"{tab_name.lower()}s": subtypes, "tab_name": tab_name},
    )

def regions_list(request, tab_name):
    regions = Region.objects.all()
    return render(
        request,
        'regions_list.html',
        context = {'regions': regions, 'tab_name': tab_name},
    )

def get_regions_api(request):
    data = request.GET['data'][0]

    # Это происходит потому что sqllite не может utf-8
    # https://www.sqlite.org/faq.html#q18
    regions = list(Region.objects.all())
    regions = [reg for reg in regions if data in reg.name]
    
    return HttpResponse(serializers.serialize("json", regions))
