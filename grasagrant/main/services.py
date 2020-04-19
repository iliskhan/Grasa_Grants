import os, sys
from datetime import date, timedelta

from main.models import Type, Grant, Fz44, Fz223, DigitalEconomy, Category, Region


def clean_4science(type_grant):

    all_grants = Grant.objects.filter(grant_name=type_grant)

    for grant in all_grants:

        if grant.days:
            day = int(grant.days)
            day -= 1

            if day <= 0:
                grant.delete()
            else:
                grant.days = day
                grant.save()
                
        else:
            if grant.time + timedelta(days=183) < date.today():
                grant.delete()

    
def clean_grant(type_grant):

    all_grants = Grant.objects.filter(grant_name=type_grant)
    
    for grant in all_grants:

        if grant.time + timedelta(days=183) < date.today():
            
            grant.delete()
            

def clean_fz44():

    all_fz = Fz44.objects.all()
    
    for fz in all_fz.iterator():
        
        if fz.create_date and fz.create_date + timedelta(days=183) < date.today():                    
            fz.delete()
    

def clean_fz223():

    all_fz = Fz223.objects.all()

    for fz in all_fz.iterator():
        
        if fz.create_date and fz.create_date + timedelta(days=183) < date.today():                    
            fz.delete()
        

# def clean_digitaleconomy():

#     all_digital = DigitalEconomy.objects.all()

#     for digital in all_digital:

#         if digital.date:
            
#             if digital.date + timedelta(days=183) < date.today():
                
#                 digital.delete()
          




