import requests
from time import sleep

url = 'http://localhost:8080/api/equipment'

# Data to post
for d in "BCDEFGKLMNOPRSTYUI":
    for z in "BCDEFGKLMNOPRSTYUI":
        data = {
            'code': 1,
            'serial_number': f'00AA{z}{d}A1AA',
        }
        sleep(0.3)
        # Make a POST request to create equipment
        response = requests.post(url, json=data)
        if response.status_code == 200:
            print('Equipment created successfully')
        else:
            print(f'Equipment creation failed with status {response.status_code}')
