import os
import json

import xml.etree.ElementTree as ET

def retrieve(path, ns):

	data = dict()

	xmlData = ET.parse(path)
			
	root = xmlData.getroot()

	fcsNotificationEF = root.find('ns2:fcsNotificationEF',ns)

	data['id'] = fcsNotificationEF.find('xmlns:id',ns).text

	data['link'] = fcsNotificationEF.find('xmlns:href',ns).text

	data['purchaseNumber'] = fcsNotificationEF.find('xmlns:purchaseNumber',ns).text

	data['purchaseObject'] = fcsNotificationEF.find('xmlns:purchaseObjectInfo',ns).text

	data['orgName'] = fcsNotificationEF.find('xmlns:purchaseResponsible/'
											 'xmlns:responsibleOrg/'
											 'xmlns:fullName',ns).text

	data['placingWay'] = fcsNotificationEF.findtext('xmlns:placingWay/'
													'xmlns:name',
													namespaces=ns)

	procedureInfo = fcsNotificationEF.find('xmlns:procedureInfo/'
										   'xmlns:collecting',
										   ns)

	data['startDate'] = procedureInfo.find('xmlns:startDate',ns).text

	data['endDate'] = procedureInfo.find('xmlns:endDate',ns).text 

	data['place'] = procedureInfo.find('xmlns:place',ns).text

	lot = fcsNotificationEF.find('xmlns:lot',ns)

	data['maxPrice'] = lot.find('xmlns:maxPrice',ns).text

	data['currency'] = lot.find('xmlns:currency/'
								'xmlns:code',ns).text

	data['financeSource'] = lot.find('xmlns:financeSource',ns).text

	customerRequirement = lot.find('xmlns:customerRequirements/'
								   'xmlns:customerRequirement',ns)

	data['applicationGuarantee'] = customerRequirement.findtext('xmlns:applicationGuarantee/'
																'xmlns:amount',
																namespaces=ns)

	data['contractGuarantee'] = customerRequirement.findtext('xmlns:contractGuarantee/'
															 'xmlns:amount',
															 namespaces=ns)

	data['delivery'] = customerRequirement.findtext('xmlns:kladrPlaces/'
												'xmlns:kladrPlace/'
												'xmlns:kladr/'
												'xmlns:fullName',
												namespaces=ns)

	data['deliveryPlace'] = customerRequirement.findtext('xmlns:kladrPlaces/'
													 'xmlns:kladrPlace/'
													 'xmlns:deliveryPlace',
													 namespaces=ns)

	return data

def main():

	path = '../data/44/'

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	data = []
	for i in os.listdir(path):

		file_path = os.path.join(path,i)
		
		if i.endswith('.xml') and i.startswith('fcsNotificationEA44'):

			data.append(retrieve(file_path, ns))

		if i != '.gitkeep':
			os.remove(file_path)

	with open(f'{path}/info.json','w',encoding='utf8') as f:
		json.dump(data, f, ensure_ascii=False, indent=4) 
if __name__ == '__main__':
	main()