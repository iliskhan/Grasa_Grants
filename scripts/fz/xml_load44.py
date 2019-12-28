import os
import datetime
import shutil

from tqdm import tqdm
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as ET


def get_44_fz(ftp, folder):

	files = ftp.nlst()

	today_date = datetime.date.today()
	lastdate = today_date - datetime.timedelta(days=20)

	print("\nПолучение файлов 44 фз")
	for file in tqdm(files):
		if file.endswith('.xml.zip'):
			splited_name = file.split('_')

			start_date = splited_name[-3][0:8]

			date = datetime.datetime.strptime(start_date, '%Y%m%d').date()

			if date >= lastdate and date <= today_date:
				with open(f'{folder}{file}','wb') as f:
					ftp.retrbinary(f'RETR {file}',f.write)

def clean_dir(path):

	print("\nОчистка устаревших данных")

	for file in tqdm(os.listdir(path)):
		if file != '.gitkeep':
			os.remove(os.path.join(path, file))


def get_relevant_files(folder_path):

	ns = {'xmlns':'http://zakupki.gov.ru/oos/types/1',
		  'ns2':'http://zakupki.gov.ru/oos/export/1'}

	print('Удаление не актуальных файлов\n')

	file_names = {
		'fcsNotificationEA44': 'ns2:fcsNotificationEF',
		'fcsNotificationZK44': 'ns2:fcsNotificationZK',
		'fcsNotificationZP44': 'ns2:fcsNotificationZP',
		'fcsNotificationOK44': 'ns2:fcsNotificationOK',
	}

	for i in tqdm(os.listdir(folder_path)):
		file_path = os.path.join(folder_path, i)

		today = datetime.date.today()

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

	print("\nРазархивирование файлов")

	if file_name.endswith('.zip'):

		zip_file = os.path.join(folder, file_name)
		with ZipFile(zip_file,'r') as zip_obj:
			zip_obj.extractall(path=folder)
		os.remove(zip_file)

def get_names_regions(url, LOG_PASS):

	with FTP(url) as ftp:
		ftp.login(user=LOG_PASS, passwd=LOG_PASS)
		ftp.cwd('fcs_regions/')
		list_regions = ftp.nlst()[:87]
		list_regions.remove('PG-PZ')

	return list_regions

def main():
	fz44 = '../../data/44/'

	URL = 'ftp.zakupki.gov.ru'

	LOG_PASS = 'free'

	list_regions = get_names_regions(URL, LOG_PASS)
	
	clean_dir(fz44)

	paths = dict()
	
	for region in list_regions:

		paths['fz44_notifications_currM'] = f'fcs_regions/{region}/notifications/currMonth/'
		paths['fz44_notifications_prevM'] = f'fcs_regions/{region}/notifications/prevMonth/'

		for path in paths.values():
			
			with FTP(URL) as ftp:

				ftp.login(user=LOG_PASS, passwd=LOG_PASS)

				ftp.cwd(path)

				get_44_fz(ftp, fz44)

				extract_files(fz44)

	get_relevant_files(fz44)


if __name__ == '__main__':
    main()