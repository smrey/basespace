import requests
import json

#load configuration
#json.loads("bs_config.json")
#runs/TiVAL03CP/files

response = requests.get('https://api.basespace.illumina.com/v2/projects/93304211/datasets?Limit=50',
                        headers = {"Authorization": 'Bearer <key>'},
                        allow_redirects=True)
#print(response.headers.get('content-type'))
if response.status_code != 200:
    print("error")
    print(response.status_code)
else:
    for i in (response.json().get("Items")):
        dataset_type = i.get('DatasetType').get('Name')
        dataset_name = i.get("Name")
        dataset_id = i.get("Id")
        if dataset_type == "Illumina Fastq":
            files_response = requests.get('https://api.basespace.illumina.com/v2/datasets/' + dataset_id + '/files?extensions=fastq.gz&Limit=1000',
                        headers = {"Authorization": 'Bearer <key>'},
                        allow_redirects=True)
            if files_response.status_code != 200:
                print('error')
                print(files_response.status_code)
            else:
                for j in files_response.json().get('Items'):
                    file_link_str = j.get('HrefContent')
                    print(file_link_str)
                    file_name = j.get('Name')
                    print(file_name)
                    file_link = requests.get(file_link_str,
                                        headers = {"Authorization": 'Bearer <key>'},
                                        allow_redirects=True, stream=True)
                    with open(file_name, 'wb') as f:
                        for chunk in file_link:
                            f.write(chunk)