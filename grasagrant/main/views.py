from main.models import Type, Grant, Fcp, Fz44, Fz223, Category, Region, DigitalEconomy

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers

from django.utils.encoding import iri_to_uri

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

def region_subtypes_list(request, tab_name, region, pk):
    category = Category.objects.get(tab_name=tab_name)
    types = Type.objects.filter(category=category)
    
    region = region.replace('_', ' ')

    subtype_name = f"{tab_name.lower()}_name"
    
    kwargs = {subtype_name: pk}
    subtypes = global_variables[tab_name].objects.filter(**kwargs)

    region = Region.objects.get(name=region)

    subtypes = subtypes.filter(region=region)

    return render(
        request,
        f'{tab_name.lower()}_list.html',
        context={f"{tab_name.lower()}s": subtypes, "tab_name": tab_name},
    )

def region_types_list(request, tab_name, region):
    
    category = Category.objects.get(tab_name=tab_name)
    types = Type.objects.filter(category=category)

    return render(
        request,
        f'region_types_list.html',
        context={f"types": types, "tab_name": tab_name, "region": region},
    )

def regions_list(request, tab_name):
    regions = Region.objects.all()
    
    regions = [(region, region.name.replace(' ','_')) for region in regions]
    
    return render(
        request,
        'regions_list.html',
        context = {'regions': regions, 'tab_name': tab_name},
    )
