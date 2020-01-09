import os
import sys
import xml.etree.ElementTree as ET
import datetime

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Fz223, Region

def retrieve(file_path):

    notice_type_dict = {
        'purchaseNotice':'Извещение о закупке "Иной способ"',
        'purchaseNoticeAE':'Извещение о закупке "Открытый аукцион в электронной форме"',
        'purchaseNoticeOA':'Извещение о закупке "Открытый Аукцион"',
        'purchaseNoticeOK':'Извещение о закупке "Открытый конкурс"',
        'purchaseNoticeZK':'Извещение о закупке "Запрос котировок"',
        'purchaseNoticeAESMBO':'Извещение о закупке "Аукцион в ЭФ, участниками которого могут являться только субъекты МСП"',
        'purchaseNoticeZKESMBO':'Извещение о закупке "Запрос котировок в ЭФ, участниками которого могут являться только субъекты МСП"',
        'purchaseNoticeKESMBO':'Извещение о закупке "Конкурс в ЭФ, участниками которого могут являться только субъекты МСП"',
        'purchaseNoticeZPESMBO':'Извещение о закупке "Запрос предложений в ЭФ, участниками которого могут являться только субъекты МСП"'
    }


    ns = {'xmlns':'http://zakupki.gov.ru/223fz/types/1',
          'ns2':'http://zakupki.gov.ru/223fz/purchase/1'}
    
    xmlData223 = ET.parse(file_path)

    root = xmlData223.getroot()

    notice_type = str(root).split('}')[-1].split('\'')[0]

    item = root.find('ns2:body/'
                     'ns2:item', ns)

    purchaseNotice = item.find(f'ns2:{notice_type}Data', ns)

    pk = Category.objects.get(tab_name='Fz223').pk   
    types = Type.objects.filter(category=pk)

    fz223 = Fz223()

    fz223.fz = types.get(name=notice_type_dict.get(notice_type))

    fz223.registration_number = purchaseNotice.find('ns2:registrationNumber', ns).text
    
    createdate = purchaseNotice.find('ns2:createDateTime', ns).text.split('T')[0]
    createdate = datetime.datetime.strptime(createdate, '%Y-%m-%d').date()
    
    fz223.create_date = createdate

    fz223.url_EIS = purchaseNotice.findtext('ns2:urlEIS', namespaces = ns)

    fz223.ulr_VSRZ = purchaseNotice.findtext('ns2:urlVSRZ', namespaces = ns)

    fz223.name = purchaseNotice.find('ns2:name', ns).text

    fz223.full_name = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:fullName', ns).text

    fz223.legal_address = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:legalAddress', ns).text

    fz223.purchase_code_name = purchaseNotice.find('ns2:purchaseCodeName', ns).text

    fz223.place = purchaseNotice.findtext('ns2:documentationDelivery/'
                                            'xmlns:place', namespaces=ns)

    lot = purchaseNotice.find('ns2:lots/'
                              'xmlns:lot/'
                              'xmlns:lotData', ns)
                  
    fz223.currency = lot.find('xmlns:currency/'
                                'xmlns:code', ns).text

    fz223.initial_sum = lot.findtext('xmlns:initialSum', namespaces=ns)

    start_date = purchaseNotice.findtext('ns2:applSubmisionStartDate', namespaces=ns)
    if start_date: fz223.submission_start_date = start_date.split('T')[0]

    close_date = purchaseNotice.findtext('ns2:submissionCloseDateTime', namespaces=ns)
    if close_date: fz223.submission_close_date = close_date.split('T')[0]
    
    region_name = purchaseNotice.find('ns2:customer/'
                                         'xmlns:mainInfo/'
                                         'xmlns:legalAddress', ns).text.split(',')[1].strip()
    
    region_list = Region.objects.all()
    region_list = [i.name for i in region_list]
    region_orm = ''

    reg_name = region_name.title()
    
    for reg in region_list:
        if reg_name in reg:
            region_orm = reg
    
    if region_orm == '':
        reg_name = region_name.split()[1].title()

        for reg in region_list:
            if reg_name in reg:
                region_orm = reg

    if region_orm == '':
        reg_name = region_name.split()[0].title()

        for reg in region_list:
            if reg_name in reg:
                region_orm = reg    
    
    region = Region.objects.get(name=region_orm)

    fz223.region = region

    fz223.save()


def main():
    path = '../data/223/'

    Fz223.objects.all().delete()

    for i in os.listdir(path):

        file_path = os.path.join(path, i)

        if i.endswith('.xml') and i.startswith('purchaseNotice'):
            retrieve(file_path)

        if i != '.gitkeep':
            os.remove(file_path)

if __name__ == '__main__':
    main()
