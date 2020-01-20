import os, sys
from datetime import date, timedelta

sys.path.append('../')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Type, Grant, Fcp, Fz44, Fz223, DigitalEconomy, Category, Region

class CleanGrant():

    @staticmethod
    def clean_4science(type_grant):

        all_grants = Grant.objects.filter(grant_name=type_grant)

        for grant in all_grants:

            if grant.days:
                day = int(grant.days)

                if day - 1 < 0:
                    grant.delete()
                else:
                    grant.days = day - 1
                    grant.save()

    @staticmethod
    def clean(type_grant):

        all_grants = Grant.objects.filter(grant_name=type_grant)
        
        for grant in all_grants:

            if grant.time + timedelta(days=183) < date.today():
                
                grant.delete()
                
class CleanFZ():

    @staticmethod
    def clean_fz44():

        all_fz = Fz44.objects.all()

        for fz in all_fz:
            
            if fz.create_date:

                if fz.create_date + timedelta(days=183) < date.today():                    
                    fz.delete()
    
    @staticmethod
    def clean_fz223():

        all_fz = Fz223.objects.all()

        for fz in all_fz:
            
            if fz.create_date:

                if fz.create_date + timedelta(days=183) < date.today():                    
                    fz.delete()
            

class CleanDigitalEconomy():

    @staticmethod
    def clean():

        all_digital = DigitalEconomy.objects.all()

        for digital in all_digital:

            if digital.date:

                if digital.date + timedelta(days=183) < date.today():
                    
                    digital.delete()
          




