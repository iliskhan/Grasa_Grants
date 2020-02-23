import os
import shutil
import datetime

from tqdm import tqdm
from ftplib import FTP
from zipfile import ZipFile

import xml.etree.ElementTree as ET


ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

def get_44_fz(ftp, folder):

	files = ftp.nlst()

	today_date = datetime.date.today()
	lastdate = today_date - datetime.timedelta(days=1)

	for file in files:
		if file.endswith('.xml.zip'):
			splited_name = file.split('_')

			start_date = splited_name[-3][0:8]

			date = datetime.datetime.strptime(start_date, '%Y%m%d').date()

			if date >= lastdate and date <= today_date:
				with open(f'{folder}{file}','wb') as f:
					ftp.retrbinary(f'RETR {file}',f.write)

def clean_dir(path):

	print("\nОчистка устаревших данных - fz44")

	for file in os.listdir(path):
		if file != '.gitkeep':
			os.remove(os.path.join(path, file))


def get_relevant_files(folder_path):

	print('Удаление не актуальных файлов - fz44\n')

	file_names = {
		'fcsNotificationEA44': 'ns2:fcsNotificationEF',
		'fcsNotificationZK44': 'ns2:fcsNotificationZK',
		'fcsNotificationZP44': 'ns2:fcsNotificationZP',
		'fcsNotificationOK44': 'ns2:fcsNotificationOK',
	}

	today = datetime.date.today()

	for i in os.listdir(folder_path):
		file_path = os.path.join(folder_path, i)

		file_name = i.split('_')[0]
		
		if i.endswith('xml') and file_name in file_names.keys():
			
			xml_file = ET.parse(file_path)
			root = xml_file.getroot()

			name_space = file_names.get(file_name)

			if name_space:
				fcsNotification = root.find(name_space, ns)

			endDate = fcsNotification.find('xmlns:procedureInfo/'
										   'xmlns:collecting/'
										    'xmlns:endDate', ns).text

			date_from_xml = endDate.split('T')[0].replace('-', '')
			
			date = datetime.datetime.strptime(date_from_xml, '%Y%m%d').date()

			if (date < today):
				os.remove(file_path)								

		if i.endswith('xml') and i.startswith('fcsNotificationINM111'):
			
			xml_file = ET.parse(file_path)
			root = xml_file.getroot()

			endDate = root.find('ns2:fcsNotification111/'
								'xmlns:procedureInfo/'
								'xmlns:collectingEndDate', ns).text
			
			date_from_xml = endDate.split('T')[0].replace('-', '')
			
			date = datetime.datetime.strptime(date_from_xml, '%Y%m%d').date()

			if (date < today):
				os.remove(file_path)

def extract_files(folder):

	print("\nРазархивирование файлов - fz44")

	for file_name in os.listdir(folder):

		if file_name.endswith('.zip'):

			zip_file = os.path.join(folder, file_name)

			with ZipFile(zip_file, 'r') as zip_obj:
				zip_obj.extractall(path=folder)

			os.remove(zip_file)


def main():
	
	fz44 = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data', '44', '')
	
	URL = 'ftp.zakupki.gov.ru'

	LOG_PASS = 'free'

	clean_dir(fz44)

	paths = dict()
	with FTP(URL) as ftp:

		ftp.login(user=LOG_PASS, passwd=LOG_PASS)

		list_regions = []
		unnecessary_folders = ["PG-PZ", "_logs", "control99docs", "fcs_undefined"]

		def folder_name_selector(some_str):
			if some_str.startswith('d'):
				folder_name = some_str.split()[-1]
				if folder_name not in unnecessary_folders:
					list_regions.append(folder_name)

		
		ftp.dir('fcs_regions/', folder_name_selector)
		print(list_regions)

		print("\nПолучение файлов - fz44")

		for region in list_regions:

			print(region)

			paths['fz44_notifications_currM'] = f'fcs_regions/{region}/notifications/currMonth/'
			paths['fz44_notifications_prevM'] = f'fcs_regions/{region}/notifications/prevMonth/'

			for path in paths.values():

				ftp.cwd(path)
				get_44_fz(ftp, fz44)

				ftp.cwd('../../../..')

	extract_files(fz44)

if __name__ == '__main__':
    main()