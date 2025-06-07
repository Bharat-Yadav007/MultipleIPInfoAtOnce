import csv
import requests

def get_ip_info(ip_address):
    url = f"https://ipinfo.io/{ip_address}/json"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            'IP': data.get('ip'),
            'City': data.get('city'),
            'Region': data.get('region'),
            'Country': data.get('country'),
            'Location': data.get('loc'),
            'Org': data.get('org'),
            'Timezone': data.get('timezone'),
            'Hostname': data.get('hostname')
        }
    else:
        return {
            'IP': ip_address,
            'Error': f"Failed to fetch data (status {response.status_code})"
        }

def process_ips_from_csv(input_file, output_file):
    with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
        reader = csv.DictReader(csv_in)
        fieldnames = ['IP', 'City', 'Region', 'Country', 'Location', 'Org', 'Timezone', 'Hostname', 'Error']
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ip = row['ip']
            info = get_ip_info(ip)
            writer.writerow(info)

# Run the function
process_ips_from_csv('IPs.csv', 'IPsInfo.csv')
print("Done! Results saved to IPsInfo.csv")
