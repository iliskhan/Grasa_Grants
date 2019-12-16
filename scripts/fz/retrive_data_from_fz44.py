import os
import sys
import xml.etree.ElementTree as ET

sys.path.append('../../grasagrant')

os.environ['DJANGO_SETTINGS_MODULE'] = 'grasagrant.settings'
import django
django.setup()

from main.models import Category, Type, Fz44

# Запрос котировок
# Запрос предложений
# Электоронный аукцион
def retrieve_EA44_ZK_ZP(file_path):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	xmlData = ET.parse(file_path)

	root = xmlData.getroot()
	
	name = file_path.split('_')[0].split('/')[-1]
	if name == 'fcsNotificationEA44':
		fcsNotification = root.find('ns2:fcsNotificationEF', ns)
	if name == 'fcsNotificationZK44':
		fcsNotification = root.find('ns2:fcsNotificationZK', ns)
	if name == 'fcsNotificationZP44':
		fcsNotification = root.find('ns2:fcsNotificationZP', ns)

	pk = Category.objects.get(tab_name='Fz44').pk
	types = Type.objects.filter(category=pk)
	fz44 = Fz44()	
	
	if name == 'fcsNotificationEA44':
		fz44.fz = types.get(name='Извещение о закупке "Электронный аукцион"')
	if name == 'fcsNotificationZK44':
		fz44.fz = types.get(name='Извещение о закупке "Запрос котировок"')
	if name == 'fcsNotificationZP44':
		fz44.fz = types.get(name='Извещение о закупке "Запрос предложений"')

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
	fz44.max_price = lot.find('xmlns:maxPrice', ns).text
	fz44.currency = lot.find('xmlns:currency/'
								'xmlns:code', ns).text
	fz44.finance_source = lot.find('xmlns:financeSource', ns).text
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

	fz44.save()												 

# Открытый конкурс
# Извещение по статье 111 44-ФЗ
def retrive_INM111_OK(file_path):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	xmlData = ET.parse(file_path)

	root = xmlData.getroot()
	
	name = file_path.split('_')[0].split('/')[-1]
	if name == 'fcsNotificationOK44':
		fcsNotification = root.find('ns2:fcsNotificationOK', ns)
	if name == 'fcsNotificationINM111':
		fcsNotification = root.find('ns2:fcsNotification111', ns)

	pk = Category.objects.get(tab_name='Fz44').pk
	types = Type.objects.filter(category=pk)
	
	fz44 = Fz44()	
	
	if name == 'fcsNotificationOK44':
		fz44.fz = types.get(name='Извещение о закупке "Открытый конкурс"')
	if name == 'fcsNotificationINM111':
		fz44.fz = types.get(name='Извещение о закупке "Закрытый аукцион с учетом положений ст. 111 ФЗ-44"')

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
	fz44.max_price = lot.find('xmlns:maxPrice',ns).text
	fz44.currency = lot.find('xmlns:currency/'
								'xmlns:code', ns).text
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

	fz44.save()

def main():

	path = '../../data/44/'

	Fz44.objects.all().delete()

	for file in os.listdir(path):

		file_path = os.path.join(path, file)

		if file.endswith('.xml') and file.startswith('fcsNotificationEA44'):
			retrieve_EA44_ZK_ZP(file_path)

		if file.endswith('.xml') and file.startswith('fcsNotificationOK44'):
			retrive_INM111_OK(file_path)

		if file.endswith('.xml') and file.startswith('fcsNotificationZK44'):
			retrieve_EA44_ZK_ZP(file_path)

		if file.endswith('.xml') and file.startswith('fcsNotificationZP44'):
			retrieve_EA44_ZK_ZP(file_path)

		if file.endswith('.xml') and file.startswith('fcsNotificationINM111'):
			retrive_INM111_OK(file_path)

		if file != '.gitkeep':
			os.remove(file_path)


if __name__ == '__main__':
	main()
