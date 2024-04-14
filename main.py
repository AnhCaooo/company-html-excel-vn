import requests
from bs4 import BeautifulSoup
import os

TEXT_FILE_NAME = 'company_info.txt'

def main(): 
	# Website URL 
	url = "https://thongtincongty.org/tp-ho-chi-minh/"
	total_pages = 1

	remove_text_if_exists()
 
	for index_page in range(total_pages): 
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
    if os.path.exists(TEXT_FILE_NAME):
        os.remove(TEXT_FILE_NAME)

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
	Appends text to a text file and have a new line right after.

	Args:
		text: The text to append to the file.
	"""
	with open(TEXT_FILE_NAME, 'a') as file:
		for key, value in dict_data.items():  
			# as 'Address - Địa chỉ is not needed, so we skip it in text file'
			if key != 'Địa chỉ:':
				file.write('%s,' % (value))
		file.write("\n")
		file.close()
    

if __name__ == "__main__":
    main() 