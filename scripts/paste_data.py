import os, sys, json

sys.path.append('../grasagrant')
os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Type, Category, Region

data = {}

with open('info.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


for value in data['category']:
    Category.objects.create(tab_name=value)

for value in data['region']:
    Region.objects.create(name=value)

for key, value in data['types'].items():

    for val in value:
        Type.objects.create(name=val, category=Category.objects.get(tab_name=key))

            
            
            
    