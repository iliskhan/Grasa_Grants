import os
import datetime

from tqdm import tqdm
from ftplib import FTP
from zipfile import ZipFile  


def get_44_fz(ftp, folder):

	files = ftp.nlst()

	yesterday, today = correct_dates()
	
	print("\nПолучение файлов 44 фз")
	for file in tqdm(files):
		if file.endswith('.xml.zip'):
			splited_name = file.split('_')
			
			start_date = splited_name[-3]
			end_date = splited_name[-2]

			if yesterday == start_date and today == end_date:

				with open(f'{folder}{file}','wb') as f:
					ftp.retrbinary(f'RETR {file}',f.write)

def clean_dir(path):

	print("\nОчистка устаревших данных")

	for file in tqdm(os.listdir(path)):
		if file != '.gitkeep':
			os.remove(os.path.join(path, file))

def correct_dates():
	date = datetime.date.today()

	today = date.strftime('%Y%m%d00')
	yesterday = date.day - 1
	yesterday = date.replace(day=yesterday)
	yesterday = yesterday.strftime('%Y%m%d00')

	return yesterday, today

def extract_files(folder):

	print("\nРазархивирование файлов")

	for file_name in tqdm(os.listdir(folder)):
		if file_name.endswith('.zip'):

			zip_file = os.path.join(folder, file_name)
			with ZipFile(zip_file,'r') as zip_obj:
				zip_obj.extractall(path=folder)
			os.remove(zip_file)

def main():
	fz44 = '../data/44/'
	fz223 = '../data/223/'

	URL = 'ftp.zakupki.gov.ru'
	
	LOG_PASS = 'free'

	fz44_notifications = 'fcs_regions/Chechenskaja_Resp/notifications/currMonth/'

	clean_dir(fz44)

	with FTP(URL) as ftp:

		ftp.login(user=LOG_PASS, passwd=LOG_PASS)

		ftp.cwd(fz44_notifications)

		get_44_fz(ftp, fz44)

		extract_files(fz44)

	
if __name__ == '__main__':
	main()