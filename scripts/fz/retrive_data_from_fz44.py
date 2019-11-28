import os
import json

import xml.etree.ElementTree as ET

# Закупка у единственного поставщика
# Запрос котировок
# Запрос предложений
# Электоронный аукцион
def retrieve_EA44_EP_ZK_ZP(file_path):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	data = dict()

	xmlData = ET.parse(file_path)

	root = xmlData.getroot()

	name = file_path.split('_')[1].split('/')[1]
	if name == 'fcsNotificationEA44':
		fcsNotification = root.find('ns2:fcsNotificationEF', ns)
	if name == 'fcsNotificationEP44':
		fcsNotification = root.find('ns2:fcsNotificationEP', ns)
	if name == 'fcsNotificationZK44':
		fcsNotification = root.find('ns2:fcsNotificationZK', ns)
	if name == 'fcsNotificationZP44':
		fcsNotification = root.find('ns2:fcsNotificationZP', ns)

	data['id'] = fcsNotification.find('xmlns:id', ns).text
	data['link'] = fcsNotification.find('xmlns:href', ns).text
	data['purchaseNumber'] = fcsNotification.find('xmlns:purchaseNumber', ns).text
	data['purchaseObject'] = fcsNotification.find('xmlns:purchaseObjectInfo', ns).text
	data['orgName'] = fcsNotification.find('xmlns:purchaseResponsible/'
											 	'xmlns:responsibleOrg/'
											 	'xmlns:fullName', ns).text
	data['placingWay'] = fcsNotification.findtext('xmlns:placingWay/'
													   'xmlns:name', namespaces=ns)
	data['startDate'] = fcsNotification.findtext('xmlns:procedureInfo/'
										   			  'xmlns:collecting/'
										   			  'xmlns:startDate', namespaces=ns)
	data['endDate'] = fcsNotification.findtext('xmlns:procedureInfo/'
										 			'xmlns:collecting/'
										 			'xmlns:endDate', namespaces=ns)
	data['place'] = fcsNotification.findtext('xmlns:procedureInfo/'
									   			  'xmlns:collecting/'
									   			  'xmlns:place', namespaces=ns)
	lot = fcsNotification.find('xmlns:lot', ns)
	data['maxPrice'] = lot.find('xmlns:maxPrice', ns).text
	data['currency'] = lot.find('xmlns:currency/'
								'xmlns:code', ns).text
	data['financeSource'] = lot.find('xmlns:financeSource', ns).text
	customerRequirement = lot.find('xmlns:customerRequirements/'
								   'xmlns:customerRequirement', ns)
	data['applicationGuarantee'] = customerRequirement.findtext('xmlns:applicationGuarantee/'
																'xmlns:amount', namespaces=ns)
	data['contractGuarantee'] = customerRequirement.findtext('xmlns:contractGuarantee/'
															 'xmlns:amount', namespaces=ns)
	data['delivery'] = customerRequirement.findtext('xmlns:kladrPlaces/'
													'xmlns:kladrPlace/'
													'xmlns:kladr/'
													'xmlns:fullName', namespaces=ns)
	data['deliveryPlace'] = customerRequirement.findtext('xmlns:kladrPlaces/'
													 'xmlns:kladrPlace/'
													 'xmlns:deliveryPlace', namespaces=ns)
	return data


# Открытый конкурс
#  извещение по статье 111 44-ФЗ
def retrive_INM111_OK(file_path):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	data = dict()

	xmlData = ET.parse(file_path)

	root = xmlData.getroot()

	name = file_path.split('_')[1].split('/')[1]
	if name == 'fcsNotificationOK44':
		fcsNotification = root.find('ns2:fcsNotificationOK', ns)
	if name == 'fcsNotificationINM111':
		fcsNotification = root.find('ns2:fcsNotification111', ns)

	data['id'] = fcsNotification.find('xmlns:id', ns).text
	data['link'] = fcsNotification.find('xmlns:href', ns).text
	data['purchaseNumber'] = fcsNotification.find('xmlns:purchaseNumber', ns).text
	data['purchaseObject'] = fcsNotification.find('xmlns:purchaseObjectInfo', ns).text
	data['orgName'] = fcsNotification.find('xmlns:purchaseResponsible/'
											 'xmlns:responsibleOrg/'
											 'xmlns:fullName', ns).text
	data['placingWay'] = fcsNotification.findtext('xmlns:placingWay/'
													'xmlns:name', namespaces=ns)

	if name == 'fcsNotificationOK44':
		data['startDate'] = fcsNotification.findtext('xmlns:procedureInfo/'
										   			 'xmlns:collecting/'
										   			 'xmlns:startDate', namespaces=ns)
		data['endDate'] = fcsNotification.findtext('xmlns:procedureInfo/'
										 		   'xmlns:collecting/'
										 	   	   'xmlns:endDate', namespaces=ns)
		data['place'] = fcsNotification.findtext('xmlns:procedureInfo/'
									   			 'xmlns:collecting/'
									   			 'xmlns:place', namespaces=ns)
	if name == 'fcsNotificationINM111':
		data['endDate'] = fcsNotification.find('xmlns:procedureInfo/'
											   'xmlns:collectingEndDate', ns).text
	lot = fcsNotification.find('xmlns:lots/'
								 'xmlns:lot', ns)
	data['maxPrice'] = lot.find('xmlns:maxPrice',ns).text
	data['currency'] = lot.find('xmlns:currency/'
								'xmlns:code', ns).text
	data['financeSource'] = lot.findtext('xmlns:financeSource',namespaces=ns)

	data['applicationGuarantee'] = fcsNotification.findtext('xmlns:customerRequirements/'
								   								'xmlns:customerRequirement/'
								   								'xmlns:applicationGuarantee/'
																'xmlns:amount', namespaces=ns)
	data['contractGuarantee'] = fcsNotification.findtext('xmlns:customerRequirements/'
								   							 'xmlns:customerRequirement/'
															 'xmlns:contractGuarantee/'
															 'xmlns:amount', namespaces=ns)
	data['delivery'] = fcsNotification.findtext('xmlns:customerRequirements/'
								   					'xmlns:customerRequirement/'
													'xmlns:kladrPlaces/'
													'xmlns:kladrPlace/'
													'xmlns:kladr/'
													'xmlns:fullName', namespaces=ns)
	data['deliveryPlace'] = fcsNotification.findtext('xmlns:customerRequirements/'
								   						'xmlns:customerRequirement/'
														'xmlns:kladrPlaces/'
													 	'xmlns:kladrPlace/'
													 	'xmlns:deliveryPlace', namespaces=ns)
	return data

def main():

	path = '../../data/44/all_files/'

	path_EA44 = '../../data/44/data_EA44/'
	path_OK44 = '../../data/44/data_OK/'
	path_ZK44 = '../../data/44/data_ZK/'
	path_ZP44 = '../../data/44/data_ZP/'
	path_EP44 = '../../data/44/data_EP/'
	path_INM111 = '../../data/44/data_INM111/'

	data_EA44 = []
	data_OK44 = []
	data_ZK44 = []
	data_ZP44 = []
	data_EP44 = []
	data_INM111 = []


	for file in os.listdir(path):

		file_path = os.path.join(path, file)

		if file.endswith('.xml') and file.startswith('fcsNotificationEA44'):
			data_EA44.append(retrieve_EA44_EP_ZK_ZP(file_path))

		if file.endswith('.xml') and file.startswith('fcsNotificationOK44'):
			data_OK44.append(retrive_INM111_OK(file_path))

		if file.endswith('.xml') and file.startswith('fcsNotificationZK44'):
			data_ZK44.append(retrieve_EA44_EP_ZK_ZP(file_path))

		if file.endswith('.xml') and file.startswith('fcsNotificationZP44'):
			data_ZP44.append(retrieve_EA44_EP_ZK_ZP(file_path))

		if file.endswith('.xml') and file.startswith('fcsNotificationEP44'):
			data_EP44.append(retrieve_EA44_EP_ZK_ZP(file_path))

		if file.endswith('.xml') and file.startswith('fcsNotificationINM111'):
			data_INM111.append(retrive_INM111_OK(file_path))

		if file != '.gitkeep':
			os.remove(file_path)


	with open(f'{path_EA44}/infoEA44.json','w',encoding='utf8') as f:
		json.dump(data_EA44, f, ensure_ascii=False, indent=4)

	with open(f'{path_OK44}/infoOK.json','w',encoding='utf8') as f:
		json.dump(data_OK44, f, ensure_ascii=False, indent=4)

	with open(f'{path_ZK44}/infoZK.json','w',encoding='utf8') as f:
		json.dump(data_ZK44, f, ensure_ascii=False, indent=4)

	with open(f'{path_ZP44}/infoZP.json','w',encoding='utf8') as f:
		json.dump(data_ZP44, f, ensure_ascii=False, indent=4)

	with open(f'{path_EP44}/infoEP.json','w',encoding='utf8') as f:
		json.dump(data_EP44, f, ensure_ascii=False, indent=4)

	with open(f'{path_INM111}/infoINM111.json','w',encoding='utf8') as f:
		json.dump(data_INM111, f, ensure_ascii=False, indent=4)


if __name__ == '__main__':
	main()
