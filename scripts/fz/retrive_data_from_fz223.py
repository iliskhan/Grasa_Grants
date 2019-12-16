import os
import sys
import xml.etree.ElementTree as ET
import datetime

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Fz223

def retrieve(file_path):

    ns = {'xmlns':'http://zakupki.gov.ru/223fz/types/1',
          'ns2':'http://zakupki.gov.ru/223fz/purchase/1'}
    
    xmlData223 = ET.parse(file_path)

    root = xmlData223.getroot()

    name = file_path.split('_')[0].split('/')[-1]

    item = root.find('ns2:body/'
                     'ns2:item', ns)

    if name == 'purchaseNotice':
        purchaseNotice = item.find('ns2:purchaseNoticeData', ns)
    if name == 'purchaseNoticeAE':
        purchaseNotice = item.find('ns2:purchaseNoticeAEData', ns)
    if name == 'purchaseNoticeOA':
        purchaseNotice = item.find('ns2:purchaseNoticeOAData', ns)
    if name == 'purchaseNoticeOK':
        purchaseNotice = item.find('ns2:purchaseNoticeOKData', ns)
    if name == 'purchaseNoticeZK':
        purchaseNotice = item.find('ns2:purchaseNoticeZKData', ns)
    if name == 'purchaseNoticeAESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeAESMBOData', ns)
    if name == 'purchaseNoticeZKESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeZKESMBOData', ns)
    if name == 'purchaseNoticeKESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeKESMBOData', ns)
    if name == 'purchaseNoticeZPESMBO':
        purchaseNotice = item.find('ns2:purchaseNoticeZPESMBOData', ns)

    pk = Category.objects.get(tab_name='Fz223').pk   
    types = Type.objects.filter(category=pk)

    fz223 = Fz223()

    if name == 'purchaseNotice':
       fz223.fz = types.get(name='Извещение о закупке "Иной способ"')

    if name == 'purchaseNoticeAE':
        fz223.fz = types.get(name='Извещение о закупке "Открытый аукцион в электронной форме"')

    if name == 'purchaseNoticeOA':
        fz223.fz = types.get(name='Извещение о закупке "Открытый Аукцион"')

    if name == 'purchaseNoticeOK':
        fz223.fz = types.get(name='Извещение о закупке "Открытый конкурс"')

    if name == 'purchaseNoticeZK':
        fz223.fz = types.get(name='Извещение о закупке "Запрос котировок"')

    if name == 'purchaseNoticeAESMBO':
        fz223.fz = types.get(name='Извещение о закупке "Аукцион в ЭФ, участниками которого могут являться только субъекты МСП"')

    if name == 'purchaseNoticeZKESMBO':
        fz223.fz = types.get(name='Извещение о закупке "Запрос котировок в ЭФ, участниками которого могут являться только субъекты МСП"')

    if name == 'purchaseNoticeKESMBO':
        fz223.fz = types.get(name='Извещение о закупке "Конкурс в ЭФ, участниками которого могут являться только субъекты МСП"')

    if name == 'purchaseNoticeZPESMBO':
        fz223.fz = types.get(name='Извещение о закупке "Запрос предложений в ЭФ, участниками которого могут являться только субъекты МСП"')  

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

    fz223.initial_sum = lot.find('xmlns:initialSum', ns).text

    start_date = purchaseNotice.findtext('ns2:applSubmisionStartDate', namespaces=ns)
    if start_date: fz223.submission_start_date = start_date.split('T')[0]

    close_date = purchaseNotice.findtext('ns2:submissionCloseDateTime', namespaces=ns)
    if close_date: fz223.submission_close_date = close_date.split('T')[0]

    fz223.save()


def main():
    path = '../../data/223/'

    Fz223.objects.all().delete()

    for i in os.listdir(path):

        file_path = os.path.join(path, i)

        if i.endswith('.xml') and i.startswith('purchaseNotice'):
            retrieve(file_path)

        if i != '.gitkeep':
            os.remove(file_path)

if __name__ == '__main__':
    main()
