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

	for i in tqdm(os.listdir(folder_path)):
		file_path = os.path.join(folder_path, i)

		today = datetime.date.today()

		names = ['fcsNotificationEA44', 'fcsNotificationZK44', 'fcsNotificationZP44', 'fcsNotificationOK44']
		
		if i.endswith('xml') and i.split('_')[0] in names:
			
			xml_file = ET.parse(file_path)
			root = xml_file.getroot()
			
			name_file = i.split('_')[0]

			if name_file == 'fcsNotificationEA44':
				fcsNotification = root.find('ns2:fcsNotificationEF', ns)
			if name_file == 'fcsNotificationZK44':
				fcsNotification = root.find('ns2:fcsNotificationZK', ns)
			if name_file == 'fcsNotificationZP44':
				fcsNotification = root.find('ns2:fcsNotificationZP', ns)
			if name_file == 'fcsNotificationOK44':
				fcsNotification = root.find('ns2:fcsNotificationOK', ns)

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

	for file_name in tqdm(os.listdir(folder)):
		if file_name.endswith('.zip'):

			zip_file = os.path.join(folder, file_name)
			with ZipFile(zip_file,'r') as zip_obj:
				zip_obj.extractall(path=folder)
			os.remove(zip_file)

def main():
	fz44 = '../../data/44/'

	URL = 'ftp.zakupki.gov.ru'

	LOG_PASS = 'free'

	paths = {'fz44_notifications_currM': 'fcs_regions/Chechenskaja_Resp/notifications/currMonth/',
			'fz44_notifications_prevM': 'fcs_regions/Chechenskaja_Resp/notifications/prevMonth/'}

	clean_dir(fz44)

	for path in paths.values():

		with FTP(URL) as ftp:

			ftp.login(user=LOG_PASS, passwd=LOG_PASS)

			ftp.cwd(path)

			get_44_fz(ftp, fz44)

			extract_files(fz44)

	get_relevant_files(fz44)


if __name__ == '__main__':
	main()
