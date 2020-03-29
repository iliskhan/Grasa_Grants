import os
import sys
import xml.etree.ElementTree as ET

from tqdm import tqdm
from datetime import date

abs_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), 'grasagrant')
sys.path.append(abs_path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Fz44, Region

from main.services import clean_fz44

# Запрос котировок
# Запрос предложений
# Электоронный аукцион
def retrieve_EA44_ZK_ZP(file_path, notification):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	xmlData = ET.parse(file_path)
	root = xmlData.getroot()
	
	name = file_path.split('_')[1].split('/')[-1]

	notification_name = notification.get(name)

	if notification_name:

		fcsNotification = root.find(f'ns2:{notification_name[0]}', ns)

		pk = Category.objects.get(tab_name='Fz44').pk
		types = Type.objects.filter(category=pk)
	
		fz44 = Fz44()	

		fz44.fz44_name = types.get(name=notification_name[1])

		fz44.create_date = date.today()

		fz44.fz44id = fcsNotification.find('xmlns:id', ns).text
		fz44.link = fcsNotification.find('xmlns:href', ns).text
		fz44.purchase_number = fcsNotification.find('xmlns:purchaseNumber', ns).text
		fz44.purchase_object = fcsNotification.find('xmlns:purchaseObjectInfo', ns).text
		fz44.org_name = fcsNotification.find('xmlns:purchaseResponsible/'
													'xmlns:responsibleOrg/'
													'xmlns:fullName', ns).text
		fz44.placing_way = fcsNotification.findtext('xmlns:placingWay/'
														'xmlns:name', namespaces=ns)
		startDate = fcsNotification.findtext('xmlns:procedureInfo/'
														'xmlns:collecting/'
														'xmlns:startDate', namespaces=ns)
		if startDate: fz44.start_date = startDate.split('T')[0] 

		endDate = fcsNotification.findtext('xmlns:procedureInfo/'
														'xmlns:collecting/'
														'xmlns:endDate', namespaces=ns)
		if endDate: fz44.end_date = endDate.split('T')[0]

		fz44.place = fcsNotification.findtext('xmlns:procedureInfo/'
													'xmlns:collecting/'
													'xmlns:place', namespaces=ns)
		lot = fcsNotification.find('xmlns:lot', ns)
		fz44.max_price = lot.findtext('xmlns:maxPrice', namespaces=ns)
		fz44.currency = lot.find('xmlns:currency/'
									'xmlns:code', ns).text
		fz44.finance_source = lot.findtext('xmlns:financeSource', namespaces=ns)
		customerRequirement = lot.find('xmlns:customerRequirements/'
									'xmlns:customerRequirement', ns)
		fz44.aplication_guarantee = customerRequirement.findtext('xmlns:applicationGuarantee/'
																	'xmlns:amount', namespaces=ns)
		fz44.contract_guarantee = customerRequirement.findtext('xmlns:contractGuarantee/'
																'xmlns:amount', namespaces=ns)
		fz44.delivery = customerRequirement.findtext('xmlns:kladrPlaces/'
														'xmlns:kladrPlace/'
														'xmlns:kladr/'
														'xmlns:fullName', namespaces=ns)
		fz44.delivery_place = customerRequirement.findtext('xmlns:kladrPlaces/'
														'xmlns:kladrPlace/'
														'xmlns:deliveryPlace', namespaces=ns)

		region_name = fcsNotification.find('xmlns:purchaseResponsible/'
												'xmlns:responsibleOrg/'
												'xmlns:factAddress', ns).text.split(',')[1:3]

		region_list = [i.name for i in Region.objects.all()]

		region_orm = region_definition(region_list, region_name)
		
		if not region_orm:
			return
		
		region = Region.objects.get(name=region_orm)
		fz44.region = region

		fz44.save()												 


# Открытый конкурс
# Извещение по статье 111 44-ФЗ
def retrive_INM111_OK(file_path, notification):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	xmlData = ET.parse(file_path)

	root = xmlData.getroot()
	
	name = file_path.split('_')[1].split('/')[-1]

	notification_name = notification.get(name)

	if notification_name:

		fcsNotification = root.find(f'ns2:{notification_name[0]}', ns)		
		pk = Category.objects.get(tab_name='Fz44').pk
		types = Type.objects.filter(category=pk)
		
		fz44 = Fz44()	

		fz44.fz44_name = types.get(name=notification_name[1])

		fz44.create_date = date.today()
		
		fz44.fz44id = fcsNotification.find('xmlns:id', ns).text
		fz44.link = fcsNotification.find('xmlns:href', ns).text
		fz44.purchase_number = fcsNotification.find('xmlns:purchaseNumber', ns).text
		fz44.purchase_object = fcsNotification.find('xmlns:purchaseObjectInfo', ns).text
		fz44.org_name = fcsNotification.find('xmlns:purchaseResponsible/'
												'xmlns:responsibleOrg/'
												'xmlns:fullName', ns).text
		fz44.placing_way = fcsNotification.findtext('xmlns:placingWay/'
														'xmlns:name', namespaces=ns)

		if name == 'fcsNotificationOK44':
			startDate = fcsNotification.findtext('xmlns:procedureInfo/'
														'xmlns:collecting/'
														'xmlns:startDate', namespaces=ns)
			if startDate: fz44.start_date = startDate.split('T')[0] 

			endDate = fcsNotification.findtext('xmlns:procedureInfo/'
													'xmlns:collecting/'
													'xmlns:endDate', namespaces=ns)
			if endDate: fz44.end_date = endDate.split('T')[0]

			fz44.place = fcsNotification.findtext('xmlns:procedureInfo/'
													'xmlns:collecting/'
													'xmlns:place', namespaces=ns)
		if name == 'fcsNotificationINM111':
			endDate = fcsNotification.findtext('xmlns:procedureInfo/'
												'xmlns:collectingEndDate', namespaces=ns)
			if endDate: fz44.end_date = endDate.split('T')[0]

		lot = fcsNotification.find('xmlns:lots/'
									'xmlns:lot', ns)
		fz44.max_price = lot.findtext('xmlns:maxPrice', namespaces=ns)
		fz44.currency = lot.findtext('xmlns:currency/'
									'xmlns:code', namespaces=ns)
		fz44.finance_source = lot.findtext('xmlns:financeSource', namespaces=ns)

		fz44.aplication_guarantee = fcsNotification.findtext('xmlns:customerRequirements/'
																	'xmlns:customerRequirement/'
																	'xmlns:applicationGuarantee/'
																	'xmlns:amount', namespaces=ns)
		fz44.contract_guarantee = fcsNotification.findtext('xmlns:customerRequirements/'
																'xmlns:customerRequirement/'
																'xmlns:contractGuarantee/'
																'xmlns:amount', namespaces=ns)
		fz44.delivery = fcsNotification.findtext('xmlns:customerRequirements/'
														'xmlns:customerRequirement/'
														'xmlns:kladrPlaces/'
														'xmlns:kladrPlace/'
														'xmlns:kladr/'
														'xmlns:fullName', namespaces=ns)
		fz44.delivery_place = fcsNotification.findtext('xmlns:customerRequirements/'
															'xmlns:customerRequirement/'
															'xmlns:kladrPlaces/'
															'xmlns:kladrPlace/'
															'xmlns:deliveryPlace', namespaces=ns)

		region_name = fcsNotification.find('xmlns:purchaseResponsible/'
												'xmlns:responsibleOrg/'
												'xmlns:factAddress', ns).text.split(',')[1:3]

		region_list = [i.name for i in Region.objects.all()]

		region_orm = region_definition(region_list, region_name)

		if not region_orm:
			return

		region = Region.objects.get(name=region_orm)
		fz44.region = region	

		fz44.save()

def region_definition(region_list, region_name):

	region_orm = ''

	region_name = [i.strip() for i in region_name if not i.strip().isdigit()]
	region_name = [i.split() for i in region_name]
	region_name = [item for sublist in region_name for item in sublist]

	remove_words = ['респ', 'обл' 'край', 'г', 'город']
	region_name = [i for i in region_name if i.lower() not in remove_words]

	for region in region_name:
		
		for reg in region_list:
			
			if region in reg:
				region_orm = reg
				break
			
	return region_orm


def main():

	notification = {
		'fcsNotificationEA44':['fcsNotificationEF', 'Извещение о закупке "Электронный аукцион"'],
		'fcsNotificationZK44':['fcsNotificationZK', 'Извещение о закупке "Запрос котировок"'],
		'fcsNotificationZP44':['fcsNotificationZP', 'Извещение о закупке "Запрос предложений"'],
		'fcsNotificationOK44':['fcsNotificationOK', 'Извещение о закупке "Открытый конкурс"'],
		'fcsNotificationINM111':['fcsNotification111', 'Извещение о закупке "Закрытый аукцион с учетом положений ст. 111 ФЗ-44"']
	}

	path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', '44', '')

	clean_fz44()

	print('Добавление данных в БД - fz44')

	for file in os.listdir(path):

		file_path = os.path.join(path, file)

		if file.endswith('.xml'):

			if file.startswith('fcsNotificationINM111') or file.startswith('fcsNotificationOK44'):
				retrive_INM111_OK(file_path, notification)

			else:
				retrieve_EA44_ZK_ZP(file_path, notification)

		if file != '.gitkeep':
			os.remove(file_path)


if __name__ == '__main__':
	main()
