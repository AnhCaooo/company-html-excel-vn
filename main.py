import requests
from bs4 import BeautifulSoup
import openpyxl

def main(): 
	# Website URL 
	url = "https://thongtincongty.org/tp-ho-chi-minh/"
	total_pages = 100

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
	filename = 'company_info.txt'
	with open(filename, 'a') as file:
		for _, value in dict_data.items():  
			file.write('%s,' % (value))
		file.write("\n")
		file.close()
    

if __name__ == "__main__":
    main() 