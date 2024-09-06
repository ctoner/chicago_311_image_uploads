import requests
import json
import prettyprint as pp

url = "http://311api.cityofchicago.org/open311/v2/requests.json"
pageload = {'page_size': 500, 'page': 1}

headers = {'Accept': 'application/vnd.github.v3+json',
			'OPEN311_API_KEY': 'YOUR API KEY HERE',}

#empty object for 311 data storage
#object to find 311 complaints with images
#marker to signify the last page in the 311 complaints
#clock to count every new identified 311 complaint with a picture

links = []
url_entry = 'media_url'
last_page = False
found_item = 0

#create end to loop — when the Chicago 311 api's list of pages run out
try:
	while not last_page:
		response = requests.get(url, headers=headers, params=pageload)
		response_dict = response.json()

		if not response_dict: #if the response is empty we've reached the last page:
			last_page = True
			print(f"No more data found. Last page processed: {pageload:['page'] -1}")
			break
#scan for 311 complaints with images
		for r in response_dict:
			link_value = r.get(url_entry)
			if link_value is not None:
				#tally up number of identified 311 complaints with URLS
				found_item += 1
				print(f"{url_entry} identified in this item. There are {found_item} 311 complaints with URLs.")
				url_data = r
				links.append(url_data)

			if link_value is None:
				continue

		#increase page number
		pageload['page'] += 1
		print(pageload['page'])

	#write the current page of media_url to file
	filename = '311_url_all.json'
	with open(filename, 'w') as f:
		json.dump(links, f, indent=4)

#in case of error, write object to the filename
except:
	
	filename = '311_url_all.json'
	with open(filename, 'w') as f:
		json.dump(links, f, indent=4)