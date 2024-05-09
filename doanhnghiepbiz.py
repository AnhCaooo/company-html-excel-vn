
# targeting website 
import csv
import os
from bs4 import BeautifulSoup
import requests


BASE_URL = 'https://doanhnghiep.biz'
OPTION_SEGMENT = 'dia-diem'
CITY_SEGMENT = 'tp-ho-chi-minh'
DISTRICT_SEGMENT = 'huyen-hoc-mon-70137'
PARENT_HTML_CONTENT_AS_TEXT = 'companies_html.txt'

COMPANY_NAME_KEY: str = 'Tên công ty'
CSV_FILE: str = 'company_info.csv'
keys_to_write = ['Tên công ty', 'Người đại diện', 'Điện thoại', 'Địa chỉ']

def main(): 
	url = '%s/%s/%s/%s' % (BASE_URL, OPTION_SEGMENT, CITY_SEGMENT, DISTRICT_SEGMENT)
	remove_text_if_exists(CSV_FILE)
	
	for index_page in range(7, 8): 
		remove_text_if_exists(PARENT_HTML_CONTENT_AS_TEXT)
		
		targeting_url = '%s/?p=%s' % (url, index_page)

		base_html_content = do_get_request_and_return_response_content(targeting_url)
		
		# Parse HTML content
		soup = BeautifulSoup(base_html_content, 'html.parser')
		for result in soup.find_all('h6'):
			endpoint = result.find('a')['href']
			append_text(endpoint, PARENT_HTML_CONTENT_AS_TEXT)

		print('get all company links from page %d already and start to get the information now!' %(index_page))
  
		links_list = read_file(PARENT_HTML_CONTENT_AS_TEXT)
		if not links_list:
			print("No lines found in the file. Something went wrong when parse HTML to string and store the file")
			return 
		for line in links_list:
			company_info = {}
			company_url = BASE_URL + line
			company_info_site = do_get_request_and_return_response_content(company_url)
			company_soup = BeautifulSoup(company_info_site, 'html.parser')
			
			company_table = company_soup.find('table', class_='company-table')
			if not company_table: 
				print("Table with class 'company-table' not found.")
				return 
				
			company_info[COMPANY_NAME_KEY] = company_table.find('th').text.strip()
			for row in company_table.find('tbody').find_all('tr'):
				# Check if there are 2 td elements and no colspan attribute
				if len(row.find_all('td')) == 2 and not row.td.has_attr('colspan'):
					key = row.find('td').text.strip()  # Get text from first td
					value = row.find_all('td')[1].text.strip()  # Get text from second td
					if value:
						company_info[key] = value.replace("\n", ".")
					else:
						company_info[key] = '' 
			append_objects_to_csv(company_info, keys_to_write, CSV_FILE)
		print('get companies info in page %d successfully' % (index_page))


def do_get_request_and_return_response_content(url: str) -> bytes:
	try:
		response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'})
		response.raise_for_status()  # Raise an error for unsuccessful requests
		return response.content
	except requests.exceptions.RequestException as e:
		print(f"Error: {e}")
		exit()

def append_text(dict_data, targeting_file):
	"""
	Appends text to a targeting file.
	"""
	with open(targeting_file, 'a', encoding='utf-8') as file:
		file.write(dict_data)
		file.write("\n")
		file.close()
	
def append_objects_to_csv(given_data, keys_to_write, targeting_file):
	# Prepare data to write (dictionary with specific key-value pairs)
	data_to_write = {key: given_data[key] for key in keys_to_write if key in given_data}
	
	with open(targeting_file, 'a', encoding="utf-8") as file: 
		# Create CSV writer object
		writer = csv.DictWriter(file, fieldnames=keys_to_write)

		# Check if the file is empty (no header row written yet)
		if file.tell() == 0:
			# Write header row if the file is empty
			writer.writeheader()

		# Write data rows
		writer.writerow(data_to_write)
		file.close()

def read_file(filename: str):
	try:
		with open(filename, 'r') as file:
			lines = file.readlines()
			# Remove trailing newlines from each line
			lines = [line.rstrip() for line in lines]
			return lines
	except FileNotFoundError:
		print(f"Error: File '{filename}' not found.")
		return []

def remove_text_if_exists(target_file):
	if os.path.exists(target_file):
		os.remove(target_file)
if __name__ == "__main__":
	main() 
 
 
 