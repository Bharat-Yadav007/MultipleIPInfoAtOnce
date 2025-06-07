import csv
import requests
from typing import Dict, Any

def getIPinfo_ipinfo_io(ip_address: str) -> Dict[str, Any]:
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
            'Hostname': data.get('hostname'),
            'Postal': data.get('postal')
        }
    else:
        return {
            'IP': ip_address,
            'Error': f"Failed to fetch data (status {response.status_code})"
        }

def getIPinfo_ip_api_com(ip_address: str) -> Dict[str, Any]:
    url = f"http://ip-api.com/json/{ip_address}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        return {
            'IP': ip_address,
            'City_ipapi': data.get('city'),
            'Region_ipapi': data.get('regionName'),
            'Country_ipapi': data.get('country'),
            'Location_ipapi': f"{data.get('lat')},{data.get('lon')}",
            'Org_ipapi': data.get('as'),
            'ISP_ipapi': data.get('isp'),
            'Timezone_ipapi': data.get('timezone'),
            'Postal_ipapi': data.get('zip')
        }
    else:
        return {
            'IP': ip_address,
            'Error_ipapi': f"Failed to fetch data (status {response.status_code})"
        }

def get_combined_ip_info(ip_address: str) -> Dict[str, Any]:    # Get data from all sources
    ipinfo_data = getIPinfo_ipinfo_io(ip_address)
    ipapi_data = getIPinfo_ip_api_com(ip_address)
    
    # Combine the data with source indicators
    combined_data = {
        'IP': ip_address,
        'City': {
            'ipinfo.io': ipinfo_data.get('City'),
            'ip-api.com': ipapi_data.get('City_ipapi')
        },
        'Region': {
            'ipinfo.io': ipinfo_data.get('Region'),
            'ip-api.com': ipapi_data.get('Region_ipapi')
        },
        'Country': {
            'ipinfo.io': ipinfo_data.get('Country'),
            'ip-api.com': ipapi_data.get('Country_ipapi')
        },
        'Location': {
            'ipinfo.io': ipinfo_data.get('Location'),
            'ip-api.com': ipapi_data.get('Location_ipapi')
        },
        'Organization': {
            'ipinfo.io': ipinfo_data.get('Org'),
            'ip-api.com': ipapi_data.get('Org_ipapi')
        },
        'Timezone': {            'ipinfo.io': ipinfo_data.get('Timezone'),
            'ip-api.com': ipapi_data.get('Timezone_ipapi')
        },        'Postal': {
            'ipinfo.io': ipinfo_data.get('Postal'),
            'ip-api.com': ipapi_data.get('Postal_ipapi')
        }
    }
    
    # Add IP-API specific fields
    combined_data['ISP'] = {'ip-api.com': ipapi_data.get('ISP_ipapi')}
    
    # Add ipinfo.io specific fields
    combined_data['Hostname'] = {'ipinfo.io': ipinfo_data.get('Hostname')}
    
    # Add any error messages
    if 'Error' in ipinfo_data:
        combined_data['Error_ipinfo'] = ipinfo_data['Error']
    if 'Error_ipapi' in ipapi_data:
        combined_data['Error_ipapi'] = ipapi_data['Error_ipapi']
        
    return combined_data

def process_ips_from_csv(input_file: str, output_file: str) -> None:
    with open(input_file, 'r') as csv_in, open(output_file, 'w', newline='') as csv_out:
        reader = csv.DictReader(csv_in)
        fieldnames = ['IP', 'ipinfo.io Data', 'ip-api.com Data', 'Errors']
        writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
        writer.writeheader()

        for row in reader:
            ip = row['ip']
            raw_info = get_combined_ip_info(ip)
            
            # Format the ipinfo.io data
            ipinfo_data = []
            if raw_info['City'].get('ipinfo.io'):
                ipinfo_data.append(f"City: {raw_info['City'].get('ipinfo.io')}")
            if raw_info['Region'].get('ipinfo.io'):
                ipinfo_data.append(f"Region: {raw_info['Region'].get('ipinfo.io')}")
            if raw_info['Country'].get('ipinfo.io'):
                ipinfo_data.append(f"Country: {raw_info['Country'].get('ipinfo.io')}")
            if raw_info['Location'].get('ipinfo.io'):
                ipinfo_data.append(f"Location: {raw_info['Location'].get('ipinfo.io')}")
            if raw_info['Organization'].get('ipinfo.io'):
                ipinfo_data.append(f"Organization: {raw_info['Organization'].get('ipinfo.io')}")
            if raw_info['Timezone'].get('ipinfo.io'):
                ipinfo_data.append(f"Timezone: {raw_info['Timezone'].get('ipinfo.io')}")
            if raw_info['Hostname'].get('ipinfo.io'):
                ipinfo_data.append(f"Hostname: {raw_info['Hostname'].get('ipinfo.io')}")
            if raw_info['Postal'].get('ipinfo.io'):
                ipinfo_data.append(f"Postal Code: {raw_info['Postal'].get('ipinfo.io')}")
            
            # Format the ip-api.com data
            ipapi_data = []
            if raw_info['City'].get('ip-api.com'):
                ipapi_data.append(f"City: {raw_info['City'].get('ip-api.com')}")
            if raw_info['Region'].get('ip-api.com'):
                ipapi_data.append(f"Region: {raw_info['Region'].get('ip-api.com')}")
            if raw_info['Country'].get('ip-api.com'):
                ipapi_data.append(f"Country: {raw_info['Country'].get('ip-api.com')}")
            if raw_info['Location'].get('ip-api.com'):
                ipapi_data.append(f"Location: {raw_info['Location'].get('ip-api.com')}")
            if raw_info['Organization'].get('ip-api.com'):
                ipapi_data.append(f"Organization: {raw_info['Organization'].get('ip-api.com')}")
            if raw_info['Timezone'].get('ip-api.com'):
                ipapi_data.append(f"Timezone: {raw_info['Timezone'].get('ip-api.com')}")
            if raw_info['ISP'].get('ip-api.com'):
                ipapi_data.append(f"ISP: {raw_info['ISP'].get('ip-api.com')}")
            if raw_info['Postal'].get('ip-api.com'):
                ipapi_data.append(f"Postal Code: {raw_info['Postal'].get('ip-api.com')}")
            
            # Collect all errors
            errors = []
            if 'Error_ipinfo' in raw_info:
                errors.append(f"ipinfo.io: {raw_info['Error_ipinfo']}")
            if 'Error_ipapi' in raw_info:
                errors.append(f"ip-api.com: {raw_info['Error_ipapi']}")
            
            # Combine all data into a single row
            info = {
                'IP': raw_info['IP'],
                'ipinfo.io Data': '\n'.join(ipinfo_data),
                'ip-api.com Data': '\n'.join(ipapi_data),
                'Errors': '\n'.join(errors) if errors else 'No Errors'
            }
                
            writer.writerow(info)

# Run the function
process_ips_from_csv('IPs.csv', 'IPsInfo.csv')
print("Done! Results saved to IPsInfo.csv")
