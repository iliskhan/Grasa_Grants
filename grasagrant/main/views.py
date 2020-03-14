from main.models import Type, Grant, Fcp, Fz44, Fz223, Category, Region, DigitalEconomy
from accounts.models import User

from itertools import chain

from django.shortcuts import redirect
from django.contrib.auth.models import Group, Permission
from django.views.generic import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, Http404
from django.core import serializers
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required, permission_required
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

    favorite_grant = request.user.grant_set.all()
    favorite_digitaleconome = request.user.digitaleconomy_set.all()
    favorite_fcp = request.user.fcp_set.all()
    favorite_fz223 = request.user.fz223_set.all()
    favorite_fz44 = request.user.fz44_set.all()

    return render(request, 'favorite_list.html', context={
                                                'favorite_grant': favorite_grant, 
                                                'favorite_digitaleconome': favorite_digitaleconome,
                                                'favorite_fcp': favorite_fcp,
                                                'favorite_fz223': favorite_fz223,
                                                'favorite_fz44': favorite_fz44
                                            })


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

# def check_user(user):
#     return user.is_superuser or user.groups.filter(name='user_subsrcibed').exists()

@login_required
@permission_required(('main.view_fz223', 'main.view_fz44'), login_url='/subscription/')
# @user_passes_test(check_user, login_url='/subscription/')
# @user_passes_test(lambda user: user.groups.filter(name='subscribers').count() == 0, login_url='home')
def regions_list(request, tab_name):
    regions = Region.objects.all()
    
    regions = [(region, region.name.replace(' ','_')) for region in regions]
    
    return render(
        request,
        'regions_list.html',
        context = {'regions': regions, 'tab_name': tab_name},
    )

def subscription(request):

    return render(request, 'subscription.html')


def buy_subscription(request):

    user_subscribed_group, create = Group.objects.get_or_create(name='user_subscribed')
    
    if create:
        permission_view_fz223 = Permission.objects.get(codename='view_fz223')
        permission_view_fz44 = Permission.objects.get(codename='view_fz44')
        user_subscribed_group.permissions.add(permission_view_fz223, permission_view_fz44)

    request.user.groups.add(user_subscribed_group)
    request.user.save()

    # view_fz223 = Permission.objects.get('main.view_fz223')
    # view_fz44 = Permission.objects.get('main.view_fz44')

    # request.user.user_permissions.add(view_fz223, view_fz44)
    # request.user.save()
    
    return render(request, 'buy_subscription.html')


