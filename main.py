import requests
from bs4 import BeautifulSoup
import os

CSV_FILE: str = 'company_info.csv'
COMPANY_NAME_KEY: str = 'Tên công ty'
COMPANY_OWNER_KEY: str = 'Đại diện pháp luật:'
COMPANY_PHONE_NUMBER_KEY: str = 'Số điện thoại:'

def main(): 
	# Website URL 
	url = "https://thongtincongty.org/tp-ho-chi-minh/"
	remove_text_if_exists()
	
	# todo: make the range more dynamic which user can specify it via cli
	for index_page in range(0, 10): 
		html_content = do_get_request_and_return_response_content(url + '/page/' + str(index_page + 1))

		# Parse HTML content
		soup = BeautifulSoup(html_content, 'html.parser')

		# Get Link data from HTML result
		for result in soup.find_all('div', class_='col post-item'):
			link = result.find('a')['href']

			company_html_content = do_get_request_and_return_response_content(link)

			# Parse HTML content
			company_soup = BeautifulSoup(company_html_content, 'html.parser')
			company_info = {}

			# Get company name 
			company_name = company_soup.find('h1', class_='entry-title').text.strip()
			company_info[COMPANY_NAME_KEY] = company_name
			
			# Get other info
			for div in company_soup.find_all('div', class_='ttdn'):
				label = div.find('label').text.strip()
				if div.find('span', class_='gia-tri'):
					value = div.find('span', class_='gia-tri').text.strip()
				elif div.find('a', class_='gia-tri'):
					value = div.find('a', class_='gia-tri').text.strip()
				company_info[label] = value

			# Append dict data to text file
			append_text(company_info)
		
		print('get company info from page %s successfully' % str(index_page + 1))

def remove_text_if_exists():
    if os.path.exists(CSV_FILE):
        os.remove(CSV_FILE)

def do_get_request_and_return_response_content(url: str) -> bytes:
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an error for unsuccessful requests
		return response.content
	except requests.exceptions.RequestException as e:
		print(f"Error: {e}")
		exit()


def append_text(dict_data):
	"""
	Appends text to a csv file.
	"""
	with open(CSV_FILE, 'a') as file:
		for key, value in dict_data.items():  
			if key == COMPANY_OWNER_KEY or key == COMPANY_PHONE_NUMBER_KEY or key == COMPANY_NAME_KEY:
				file.write('%s,' % (value))
		file.write("\n")
		file.close()
    

if __name__ == "__main__":
    main() 