import requests
from bs4 import BeautifulSoup
import pandas as pd

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
		company_info = {'Name': name, 'link': link}
		contact_info = string_to_dict(result.find('p').text.split('-')[1].strip())

		# Concat Append the data to the list
		data.append({**company_info, **contact_info})

	# Create pandas dataframe
	df = pd.DataFrame(data)

	# ! CANNOT EXPORT TO EXCEL FILE YET
	# Save to Excel file
	try:
		df.to_excel("company.xlsx", index=False)
		print("Data saved to company.xlsx")
	except pd.errors.ExcelFileError as e:
		print(f"Error saving to Excel: {e}")


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