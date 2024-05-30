import requests
import csv
import io
import argparse
import os
import logging
from datetime import datetime

# Setup logging
logging.basicConfig(filename='/path/to/dpops-log.out', level=logging.INFO, format='%(asctime)s - %(message)s')

def get_username():
    return os.getenv('USER') or os.getenv('USERNAME')

def fetch_json_data(url):
    response = requests.get(url)
    response.raise_for_status()  # Check if the request was successful
    return response.json()

def filter_and_convert_to_csv(data, admin_state, op_state):
    # Extract the list under "ObjectStatus"
    object_status_list = data.get("ObjectStatus", [])
    
    # Filter the list based on the AdminState and OpState
    filtered_list = [item for item in object_status_list if item.get("AdminState") == admin_state and item.get("OpState") == op_state]
    
    # Initialize a string buffer to hold the CSV data
    output = io.StringIO()
    
    # Define the headers for the CSV
    headers = ["Class", "Name", "OpState", "AdminState"]
    
    # Write the parsed data to the string buffer
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for item in filtered_list:
        # Create a dictionary with only the required fields
        row = {header: item.get(header, '') for header in headers}
        writer.writerow(row)
    
    # Get the CSV content as a string
    csv_content = output.getvalue()
    
    # Close the string buffer
    output.close()
    
    return csv_content

def show_enabled_and_down_csv(data):
    return filter_and_convert_to_csv(data, "enabled", "down")

if __name__ == "__main__":
    # Setup argument parsing
    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-action', required=True, help='Action name')
    parser.add_argument('-env', required=True, help='Environment name')
    args = parser.parse_args()
    
    # Log the execution
    username = get_username()
    command = f"{username} : python3 dpops.py -action {args.action} -env {args.env}"
    logging.info(command)
    
    # Example usage
    url = 'https://api.example.com/your-endpoint'
    data = fetch_json_data(url)

    enabled_and_down_csv_content = show_enabled_and_down_csv(data)

    print("Enabled and Down CSV Content:")
    print(enabled_and_down_csv_content)
