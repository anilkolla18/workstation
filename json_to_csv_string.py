import json
import csv
import io

def json_to_csv_string(json_data):
    # Parse the JSON data
    data = json.loads(json_data)
    
    # Extract the list under "ObjectStatus"
    object_status_list = data.get("ObjectStatus", [])
    
    # Initialize a string buffer to hold the CSV data
    output = io.StringIO()
    
    # Define the headers for the CSV
    headers = ["Class", "Name", "OpState", "AdminState"]
    
    # Write the parsed data to the string buffer
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for item in object_status_list:
        # Create a dictionary with only the required fields
        row = {header: item.get(header, '') for header in headers}
        writer.writerow(row)
    
    # Get the CSV content as a string
    csv_content = output.getvalue()
    
    # Close the string buffer
    output.close()
    
    return csv_content

# Example usage
json_data = '''
{
    "ObjectStatus": [
        {
            "Class": "ClassName1",
            "OpState": "up",
            "AdminState": "enabled",
            "Name": "Name1",
            "ConfigStarte": "Saved"
        },
        {
            "Class": "ClassName2",
            "OpState": "down",
            "AdminState": "enabled",
            "Name": "Name2",
            "ConfigStarte": "Saved"
        },
        {
            "Class": "ClassName3",
            "OpState": "down",
            "AdminState": "disabled",
            "Name": "Name3",
            "ConfigStarte": "Saved"
        }
    ]
}
'''

csv_content = json_to_csv_string(json_data)
print(csv_content)
