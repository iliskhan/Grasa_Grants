from main.models import Type, Grant, Fcp, Fz44, Fz223, Category, Region, DigitalEconomy
from accounts.models import User

from itertools import chain

from django.shortcuts import redirect

from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.contrib.auth.decorators import login_required, user_passes_test

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

    is_favorite = False

    data = get_object_or_404(global_variables[tab_name], id=pk)

    if data.favorite.filter(id=request.user.id).exists():
        is_favorite = True

    return render(
        request,
        f'{tab_name.lower()}.html',
        context = {'data': data,
                   'is_favorite':is_favorite},
    )

@login_required
def favorite_post(request, tab_name, pk):
    post = get_object_or_404(global_variables[tab_name], id=pk)

    if post.favorite.filter(id=request.user.id).exists():
        post.favorite.remove(request.user)
    else:
        post.favorite.add(request.user)

    return redirect(post.get_absolute_url())
    

def favorite_list(request):

    user = request.user
    
    favorite_grant = user.grant_set.all()
    favorite_digitaleconome = user.digitaleconomy_set.all()
    favorite_fcp = user.fcp_set.all()
    favorite_fz223 = user.fz223_set.all()
    favorite_fz44 = user.fz44_set.all()

    favorite_all = list(chain(favorite_grant, favorite_digitaleconome, favorite_fcp, favorite_fz223, favorite_fz44))

    
    # return HttpResponse(favorite_all[-1].__class__.__name__)
    return render(request, 'favorite_list.html', context={'favorite_all': favorite_all})


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


@user_passes_test(lambda user: user.groups.filter(name='subscribers').count() == 0, login_url='home')
def regions_list(request, tab_name):
    regions = Region.objects.all()
    
    regions = [(region, region.name.replace(' ','_')) for region in regions]
    
    return render(
        request,
        'regions_list.html',
        context = {'regions': regions, 'tab_name': tab_name},
    )



