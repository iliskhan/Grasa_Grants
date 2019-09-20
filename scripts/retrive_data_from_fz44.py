import os
import xmltodict
import pandas as pd 

import xml.etree.ElementTree as ET
from lxml import objectify

def main():

	path = '../data/44/'

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	for i in os.listdir(path):
		print(i)
		if i.endswith('.xml') and i.startswith('fcsNotificationEA44'):
			
			file_path = os.path.join(path,i)
		
			xmlData = ET.parse(file_path)
			
			root = xmlData.getroot()

			fcsNotificationEF = root.find('ns2:fcsNotificationEF', ns)

			id = fcsNotificationEF.find('xmlns:id', ns).text

			purchaseNumber = fcsNotificationEF.find('xmlns:purchaseNumber', ns).text

			purchaseObject = fcsNotificationEF.find('xmlns:purchaseObjectInfo', ns).text

			orgName = fcsNotificationEF.find('xmlns:purchaseResponsible',ns)\
									   .find('xmlns:responsibleOrg',ns)\
									   .find('xmlns:fullName',ns).text

			placingWay = fcsNotificationEF.find('xmlns:placingWay',ns)\
										  .find('xmlns:name',ns).text

			startDate = fcsNotificationEF.find('xmlns:procedureInfo',ns)\
										 .find('xmlns:collecting',ns)\
										 .find('xmlns:startDate',ns).text

			endDate = fcsNotificationEF.find('xmlns:')
			print(orgName)
			break


			

if __name__ == '__main__':
	main()