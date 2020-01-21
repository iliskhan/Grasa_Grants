import os
import datetime

from tqdm import tqdm
from ftplib import FTP
from zipfile import ZipFile
import xml.etree.ElementTree as ET


def get_223_fz(ftp, folder):
    
	files = []
	ftp.retrlines("LIST", files.append)
	
	files = [file.split(None, 8) for file in files]
	
	files_name = [file[-1] for file in files]
	files_size = [file[4] for file in files]

	#files = ftp.nlst()

	today_date = datetime.date.today()
	lastdate = today_date - datetime.timedelta(days=20)

	print("\nПолучение файлов 223 фз")

	for i in tqdm(range(len(files_name))):

		if files_name[i].endswith('.xml.zip') and int(files_size[i]) >= 1000:
			
			splited_name = files_name[i].split('_')

			date = splited_name[-6]
			date = datetime.datetime.strptime(date, '%Y%m%d').date()

			if date >= lastdate and date <= today_date:
			    with open(f'{folder}{files_name[i]}', 'wb') as f:
				    ftp.retrbinary(f'RETR {files_name[i]}', f.write)


	# for file in tqdm(files):
	# 	if file.endswith('.xml.zip'):
	# 		splited_name = file.split('_')

	# 		date = splited_name[-6]
	# 		date = datetime.datetime.strptime(date, '%Y%m%d').date()

	# 		if date >= lastdate and date <= today_date:
	# 		    with open(f'{folder}{file}', 'wb') as f:
	# 			    ftp.retrbinary(f'RETR {file}', f.write)

def del_empty_files(path_folder):

	print('\nУдаление пустых файлов по 223фз')

	for i in tqdm(os.listdir(path_folder)):
		file_path = os.path.join(path_folder, i)
		file_size = os.path.getsize(file_path)
		if i.endswith('.xml') and (file_size == 0):
			os.remove(file_path)

def get_relevant_files(path_folder):

	ns = {'xmlns':'http://zakupki.gov.ru/223fz/types/1',
	      'ns2':'http://zakupki.gov.ru/223fz/purchase/1'}

	print('\nУдаление не актуальных файлов по 223фз')

	for i in tqdm(os.listdir(path_folder)):
		file_path = os.path.join(path_folder, i)

		if i.endswith('.xml') and i.startswith('purchase'):

			xml_file = ET.parse(file_path)
			root = xml_file.getroot()

			notice = str(root)
			notice_arr = notice.split('}')
			notice = notice_arr[1].split('\'')[0]

			closeData = root.find('ns2:body/'
			                      'ns2:item/'
								  f'ns2:{notice}Data/'
								  'ns2:submissionCloseDateTime', ns).text
				  
			date_from_xml = closeData.split('T')[0].replace('-', '')
			
			today = datetime.date.today()
			date = datetime.datetime.strptime(date_from_xml, '%Y%m%d').date()

			if (date < today):
				os.remove(file_path)


def clean_dir(path):

	print("\nОчистка устаревших данных")

	for file in tqdm(os.listdir(path)):
		if file != '.gitkeep':
			os.remove(os.path.join(path, file))


def extract_files(folder):

	print("\nРазархивирование файлов")

	for file_name in tqdm(os.listdir(folder)):
		if file_name.endswith('.zip'):

			zip_file = os.path.join(folder, file_name)
			with ZipFile(zip_file,'r') as zip_obj:
				zip_obj.extractall(path=folder)
			os.remove(zip_file)

def get_names_regions(url, LOG_PASS):

	ftp = FTP(url)
	ftp.login(user=LOG_PASS, passwd=LOG_PASS)
	ftp.cwd('out/published')
	list_regions = ftp.nlst()[:87]
	list_regions.remove('Irkutskaya_obl_Ust-Ordynskii_Buriatskii_okrug')

	return list_regions

def main():

	fz223 = '../../data/223/'

	URL = 'ftp.zakupki.gov.ru'

	LOG_PASS = 'fz223free'

	list_regions = get_names_regions(URL, LOG_PASS)
	
	clean_dir(fz223)

	folder_path = dict()

	for region in list_regions:

		print(region)
		
		folder_path['fz223_notice'] = f'out/published/{region}/purchaseNotice/daily'
		folder_path['fz223_noticeAE'] = f'out/published/{region}/purchaseNoticeAE/daily/'
		folder_path['fz223_noticeAESMBO'] = f'out/published/{region}/purchaseNoticeAESMBO/daily/'
		folder_path['fz223_noticeKESMBO'] = f'out/published/{region}/purchaseNoticeKESMBO/daily/'
		folder_path['fz223_noticeOA'] = f'out/published/{region}/purchaseNoticeOA/daily/'
		folder_path['fz223_noticeOK'] = f'out/published/{region}/purchaseNoticeOK/daily/'
		folder_path['fz223_noticeZK'] = f'out/published/{region}/purchaseNoticeZK/daily/'
		folder_path['fz223_noticeZKESMBO'] = f'out/published/{region}/purchaseNoticeZKESMBO/daily/'
		folder_path['fz223_noticeZPESMBO'] = f'out/published/{region}/purchaseNoticeZPESMBO/daily/'

		for i in folder_path.values():

			with FTP(URL) as ftp:
				ftp.login(user=LOG_PASS, passwd=LOG_PASS)

				ftp.cwd(i)

				get_223_fz(ftp, fz223)

	extract_files(fz223)

	del_empty_files(fz223)
	get_relevant_files(fz223)

if __name__ == '__main__':
    main()
