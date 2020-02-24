import os, sys, json

sys.path.append('../grasagrant')
os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Type, Category, Region

data = {'category':[i.tab_name for i in Category.objects.all()],
       'region':[i.name for i in Region.objects.all()]}

types = {}

for i in data['category']:
    pk = Category.objects.get(tab_name=f'{i}').pk
    types[f'{i}'] = [i.name for i in Type.objects.filter(category=pk)]

data['types'] = types

with open('info.json', 'w', encoding='utf8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
