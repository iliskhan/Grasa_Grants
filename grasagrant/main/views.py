from django.shortcuts import render, redirect
from main.models import Type, Grant, Fcp, Fz44, Fz223, Category, Region
from django.http import HttpResponse, Http404
from django.core import serializers


# Create your views here.
def index(request):
    return redirect('grants')

def grant_types_list(request):
    category = Category.objects.get(tab_name='Grants')
    types = Type.objects.filter(category=category)
    return render(
        request,
        'types_list.html',
        context = {'types': types, 'query_to': 'grants_list'},
    )

def grants_list(request, pk):
    grants = Grant.objects.filter(grant_name=pk).order_by('-time')
    return render(
        request,
        'grants_list.html',
        context = {'grants': grants},
    )

def grant_detailed(request, pk):
    try:
        grant = Grant.objects.get(id=pk)
    except Grant.DoesNotExist:
        raise Http404("Grant does not exist")

    return render(
        request,
        'grant.html',
        context = {'grant': grant},
    )


def fcp_types_list(request):
    category = Category.objects.get(tab_name='Fcp')
    types = Type.objects.filter(category=category)
    return render(
        request,
        'types_list.html',
        context = {'types': types, 'query_to': 'fcps_list'},
    )

def fcps_list(request, pk):
    fcps = Fcp.objects.filter(gp_name=pk).order_by('-time')
    return render(
        request,
        'fcps_list.html',
        context = {'fcps': fcps},
    )

def fcp_detailed(request, pk):
    try:
        fcp = Fcp.objects.get(id=pk)
    except Fcp.DoesNotExist:
        raise Http404("Fcp does not exist")

    return render(
        request,
        'fcp.html',
        context = {'fcp': fcp},
    )


def fz44_types_list(request):
    category = Category.objects.get(tab_name='Fz44')
    types = Type.objects.filter(category=category)
    return render(
        request,
        'types_list.html',
        context = {'types': types, 'query_to': 'fz44_list'},
    )

def fz44_list(request, pk):
    fzs = Fz44.objects.filter(fz=pk)
    return render(
        request,
        'fz44_list.html',
        context = {'fzs': fzs},
    )

def fz44_detailed(request, pk):
    try:
        fz = Fz44.objects.get(id=pk)
    except Fz44.DoesNotExist:
        raise Http404("Fz44 does not exist")

    return render(
        request,
        'fz44.html',
        context = {'fz': fz},
    )


def fz223_types_list(request):
    category = Category.objects.get(tab_name='Fz223')
    types = Type.objects.filter(category=category)
    return render(
        request,
        'types_list.html',
        context = {'types': types, 'query_to': 'fz223_list'},
    )

def fz223_list(request, pk):
    fzs = Fz223.objects.filter(fz=pk)
    return render(
        request,
        'fz223_list.html',
        context = {'fzs': fzs},
    )

def fz223_detailed(request, pk):
    try:
        fz = Fz223.objects.get(id=pk)
    except Fz223.DoesNotExist:
        raise Http404("Fz223 does not exist")

    return render(
        request,
        'fz223.html',
        context = {'fz': fz},
    )

def regions_list(request):
    regions = Region.objects.all()
    return render(
        request,
        'regions_list.html',
        context = {'reigons': regions},
    )

def get_regions_api(request):
    data = request.GET['data'][0]

    # Это происходит потому что sqllite не может utf-8
    # https://www.sqlite.org/faq.html#q18
    regions = list(Region.objects.all())
    regions = [reg for reg in regions if data in reg.name]
    
    return HttpResponse(serializers.serialize("json", regions))
