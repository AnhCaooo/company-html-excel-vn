import requests
from bs4 import BeautifulSoup
import openpyxl

def main(): 
	# Website URL 
	url = "https://www.tratencongty.com/"

	# Send GET request and store content
	try:
		response = requests.get(url)
		response.raise_for_status()  # Raise an error for unsuccessful requests
		html_content = response.content
	except requests.exceptions.RequestException as e:
		print(f"Error: {e}")
		exit()

	# Parse HTML content
	soup = BeautifulSoup(html_content, 'html.parser')

	# Extract data from search results
	data = []
	for result in soup.find_all('div', class_='search-results'):
		name = result.find('a').text.strip()
		link = result.find('a')['href']
		company_info = {'Name': name, 'Link': link}
		contact_info = string_to_dict(result.find('p').text.split('-')[1].strip())

		# Concat Append the data to the list
		data.append({**company_info, **contact_info})

	# Create a workbook
	wb = openpyxl.Workbook()

	# Get the active worksheet
	ws = wb.active

	# Set column headers
	ws.cell(row=1, column=1).value = "Name"
	ws.cell(row=1, column=2).value = "Link"
	ws.cell(row=1, column=3).value = "Đại diện pháp luật"
	ws.cell(row=1, column=4).value = "Địa chỉ"

	# Iterate through the list and write data to cells
	row_num = 2
	for company_data in data:
		ws.cell(row=row_num, column=1).value = company_data['Name']
		ws.cell(row=row_num, column=2).value = company_data['Link']
		ws.cell(row=row_num, column=3).value = company_data['Đại diện pháp luật']
		ws.cell(row=row_num, column=4).value = company_data['Địa chỉ']
		row_num += 1

	# Save the workbook with a filename
	filename = "company_data.xlsx"
	wb.save(filename)

	print(f"Company data exported to Excel file: {filename}")


def string_to_dict(text: str):
	"""
	Converts a string with key-value pairs on separate lines to a dictionary.

	Args:
		text: The string containing key-value pairs.

	Returns:
		A dictionary with extracted key-value pairs.
	"""
	# Split the string by lines
	lines = text.splitlines()

	# Initialize an empty dictionary
	data = {}

	# Loop through each line
	for line in lines:
		# Remove extra whitespace and split by the first colon
		key, value = line.strip().split(":", 1)
		# Add the key-value pair to the dictionary
		data[key] = value

	return data

if __name__ == "__main__":
    main() 