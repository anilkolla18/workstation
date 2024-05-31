import requests, json, base64, sys, smtplib, io, csv
import os, logging, argparse
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime

# Setup logging
logging.basicConfig(filename='logs/dpops-log.out', level=logging.INFO, format='%(asctime)s - %(message)s')

verify_ssl = True

def send_email(subject, message):
    sender_email = "anil.kolla@mydomain.com"
    receiver_email = "anil.kolla@mydomain.com"
    smtp_server = "smtpcdc.mydomain.com"
    smtp_port = 25

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to email
    msg.attach(MIMEText(message, "plain"))

    # Send email
    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.send_message(msg)

def domains_list(base_url, headers):
        #return requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()
    domains = requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()
    domain_list = []
    for domain in domains['domain']:
        domain_list.append(domain['name'])

    return domain_list

def list_services(base_url, headers, domain, service_type):
        return requests.get(base_url + 'mgmt/config/' + domain + '/' + service_type, headers = headers, verify = verify_ssl).json()

def disable_service_probe(base_url, headers, domain, service_type, service_name):
        #return requests.put(base_url + 'mgmt/config/' + domain + '/' + service_type + '/' + service_name + '/DebugMode', data = json.dumps({ "DebugMode": "off" }), headers = headers, verify = verify_ssl).json()
    print('in disable_service_probe')

def disable_probes(datapower_ips, roma_port, username, password):
    base_url = 'https://' + datapower_ip + ':' + str(roma_port) + '/'
    headers = {'Authorization' : 'Basic ' + str(base64.b64encode((username + ':' + password).encode()).decode())}
    enabled_probes = []
    connected = False
    try:
        domains = list_domains(base_url, headers)
        connected = True
    except requests.exceptions.SSLError:
        print('Connection to ' + datapower_ip + ' failed because of a tls trust issue, you may use the -ignore-tls-issues to bypass this.', file=sys.stderr)
    except requests.ConnectionError:
        print('Connection to ' + datapower_ip + ' failed, please verify that the REST Management Interface is enabled.', file=sys.stderr)

    if connected:
        #print(domains)
        if domains.get('domain'):
            for domain in domains['domain']:
                services_types = [ 'WSGateway', 'MultiProtocolGateway' ]
                for service_type in services_types:
                    services_result = list_services(base_url, headers, domain['name'], service_type)
                    #print(services_result)
                    if services_result.get(service_type):
                        if (isinstance(services_result[service_type], list)):
                            for service in services_result[service_type]:
                                #print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
                                if service['DebugMode'] == 'on':
                                    enabled_probes.append({ 'domain': domain['name'] , 'service_type': service_type, 'service_name': service['name'] })

                        else:
                            service = services_result[service_type]
                            #print(service)
                            #print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
                            if service['DebugMode'] == 'on':
                                enabled_probes.append({ 'domain': domain['name'], 'service_type': service_type, 'service_name': service['name'] })
        print(enabled_probes)
        if not enabled_probes:
            subject = 'Probe Check on ' + datapower_ip + '.'
            message = 'No enabled Probes were found on ' + datapower_ip + '.'
            print(message)
        else:
            for probe in enabled_probes:
                print('Disabling the Probe for ' + probe['service_type'] + ' \'' + probe['service_name'] + '\' in domain \'' + probe['domain'] + '\'... ')
                r = disable_service_probe(base_url, headers, probe['domain'],  probe['service_type'], probe['service_name'])
                if (r['DebugMode'] == 'Property was updated.'):
                    print(' --> Disabled successfully!')
                    #subject = "Probes are enabled in below Domains"
                    #message = "Probes are enabled in below Domains, Please make sure to disable them if they are not in Use.\n"
                    #message += "\n".join(probe_enabled_domains)
                else:
                    print(' --> Failed!')


def getDomainsList(base_url, headers):
    print("In getDomainsList Function")
    return requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()

def getObjectStatus(base_url, headers, domainName, objectName):
    print("In getObjectStatus Function")

    if objectName == 'Statistics':
        url = base_url + 'mgmt/config/' + domainName +'/'+ objectName +'/default'
    #print(url)
    return requests.get(url, headers = headers, verify = verify_ssl).json()

def list_objects_with_status(base_url, headers, domainName):
    #print("In list_objects_with_status Function")
    url = base_url + 'mgmt/status/' + domainName +'/ObjectStatus'
    #print(url)
    return requests.get(url, headers = headers, verify = verify_ssl).json()

def createDomain(base_url, headers, domainName):
    print("In createDomain Function")

    url = base_url + 'mgmt/config/default/Domain/' + domainName

    print(url)
    request = '{ "Domain": { "name": "'+ domainName + '", "mAdminState": "enabled" } }'
    print(request)
    r = requests.put(url, data = request, headers = headers, verify = verify_ssl).json()
    #return requests.put(url, data = request, headers = headers, verify = verify_ssl).json()

    # Making a PUT request
    #r = requests.put('https://httpbin.org / put', data ={'key':'value'})
    # check status code for response received
    # success code - 200
    print(r)
    # print content of request
    #print(r.content)

def checkDomainsExistance(base_url, headers, domainName):
    #print("In checkDomainsExistance Function")
    if domainName == '':
        print("Please Provide DomainName.")
    #print("domainName Given : " +domainName)
    r = domains_list(base_url, headers)
    return domainName in r

def check_probe_status(base_url, headers, host):

    print("In check_probe_status Function")

    enabled_probes = []
    connected = False
    try:
        domains = requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()
        connected = True
    except requests.exceptions.SSLError:
        print('Connection to ' + host + ' failed because of a tls trust issue, you may use the -ignore-tls-issues to bypass this.', file=sys.stderr)
    except requests.ConnectionError:
        print('Connection to ' + host + ' failed, please verify that the REST Management Interface is enabled.', file=sys.stderr)

    if connected:
        print(domains)
        if domains.get('domain'):
            for domain in domains['domain']:
                services_types = [ 'WSGateway', 'MultiProtocolGateway' ]
                for service_type in services_types:
                    services_result = list_services(base_url, headers, domain['name'], service_type)
                    #print(services_result)
                    if services_result.get(service_type):
                        if (isinstance(services_result[service_type], list)):
                            for service in services_result[service_type]:
                                #print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
                                if service['DebugMode'] == 'on':
                                    enabled_probes.append({ 'domain': domain['name'] , 'service_type': service_type, 'service_name': service['name'] })

                        else:
                            service = services_result[service_type]
                            #print(service)
                            #print(domain['name'] + ' -> Found ' + service_type + ': ' + service['name'] + ' (Probe: ' + service['DebugMode'] + ')')
                            if service['DebugMode'] == 'on':
                                enabled_probes.append({ 'domain': domain['name'], 'service_type': service_type, 'service_name': service['name'] })
        print(enabled_probes)
        if not enabled_probes:
            subject = 'Probe Check on ' + host + '.'
            message = 'No enabled Probes were found on ' + host + '.'
            print(message)
            send_email(subject, message)
        else:
            for probe in enabled_probes:
                print('Disabling the Probe for ' + probe['service_type'] + ' \'' + probe['service_name'] + '\' in domain \'' + probe['domain'] + '\'... ')
                r = disable_service_probe(base_url, headers, probe['domain'],  probe['service_type'], probe['service_name'])
                if (r['DebugMode'] == 'Property was updated.'):
                    print(' --> Disabled successfully!')
                    subject = "Probes are enabled in below Domains"
                    message = "Probes are enabled in below Domains, Please make sure to disable them if they are not in Use.\n"
                    message += "\n".join(probe_enabled_domains)
                else:
                    print(' --> Failed!')

        send_email(subject, message)

def object_list_csv(base_url, headers, domainName, adminState, opState):

    #print("In object_list_csv Function")
    objList = list_objects_with_status(base_url, headers, domainName)
    # Extract the list under "ObjectStatus"
    object_status_list = [item for item in objList.get("ObjectStatus", []) if item.get("AdminState") == adminState and item.get("OpState") == opState]

    # Initialize a string buffer to hold the CSV data
    output = io.StringIO()

    # Define the headers for the CSV
    headers = ["Domain Name", "Class", "Name", "OpState", "AdminState"]

    # Write the parsed data to the string buffer
    writer = csv.DictWriter(output, fieldnames=headers)
    writer.writeheader()
    for item in object_status_list:
        # Create a dictionary with only the required fields
        #row = {header: item.get(header, '') for header in headers}
        row = {"Domain Name": domainName}
        row.update({header: item.get(header, '') for header in headers if header != "Domain Name"})
        writer.writerow(row)

    # Get the CSV content as a string
    csv_data = output.getvalue()

    # Close the string buffer
    output.close()

    return csv_data

def all_domain_action(base_url, headers, host, action):
    action_out = []
    connected = False
    try:
        domains = requests.get(base_url + 'mgmt/domains/config/', headers = headers, verify = verify_ssl).json()
        connected = True
    except requests.exceptions.SSLError:
        print('Connection to ' + host + ' failed because of a tls trust issue, you may use the -ignore-tls-issues to bypass this.', file=sys.stderr)
    except requests.ConnectionError:
        print('Connection to ' + host + ' failed, please verify that the REST Management Interface is enabled.', file=sys.stderr)

    if connected:
        #print(domains)
        if domains.get('domain'):
            for domain in domains['domain']:
                #Logic Here
                activeDomain = domain['name']
                #print('Working on Domain : ' +activeDomain)
                #print('Performing action : ' +action)

                if action == 'listObjects_down':
                    #action_out.extend(object_list_csv(base_url,headers, activeDomain, "enabled", "down"))
                    objList_down=object_list_csv(base_url,headers, activeDomain, "enabled", "down")
                    print(objList_down)
            #print(action_out)
def dpOperations(hosts, roma_port, username, password, action, objectName, domainName):
    for host in hosts:
        print('Working on : ' + host)
        print('Performing Action : ' + action)
        base_url = 'https://' + host + ':' + str(roma_port) + '/'
        headers = {'Authorization' : 'Basic ' + str(base64.b64encode((username + ':' + password).encode()).decode())}

        if action == 'checkDomainsExistance':
            #python dpops.py -env sbx -action checkDomainsExistance -domainName dpops
            #print("Start Action checkDomainsExistance")
            r = checkDomainsExistance(base_url, headers, domainName)
            if r:
                print('Application Domain ' + domainName + ' Exists on '+ host)
            else:
                print('Application Domain ' + domainName + ' Does not Exists on '+ host)
        if action == 'getDomainsList':
            print("Start Action getDomainsList")

            # Call Function getDomainsList() and store results on variable domains
            domains = getDomainsList(base_url, headers)
            for domain in domains['domain']:
                print(domain['name'])

            print("End Action getDomainsList")
        if action == 'getObjectStatus':
            # Call Function getObjectStatus()
            print("Start Action getObjectStatus")
            if domainName == '':
                domainName = 'default'
            objectStatus = getObjectStatus(base_url, headers, domainName, objectName)

            print(objectStatus[objectName])

            print("End Action getObjectStatus")
        if action == 'listObjects_down':

            # Call Function listObjects_down()
            #print("Start Action listObjects_down")
            if domainName == '':
                print("Please pass Domain Name.")
                return
            if domainName == 'all':
                print("Getting List in All Domains.")
                #objList_down = object_list_csv(base_url,headers, domainName, "enabled", "down")
                #print(objList_down)
                objList_down = all_domain_action(base_url, headers, host, action)
                print(objList_down)
                return
            else:
                r = checkDomainsExistance(base_url, headers, domainName)
                if not r:
                    print('Application Domain ' + domainName + ' Does not Exists on '+ host)
                    return
                #domainName = 'default'
                #objList = list_objects_with_status(base_url, headers, domainName)
                objList_down = object_list_csv(base_url,headers, domainName, "enabled", "down")
                print(objList_down)
                return

        if action == 'createDomain':
            # Call Function createDomain()
            print("Start Action createDomain")
            if domainName != '':
                print("Creating Domain : "+domainName)

                reponse = createDomain(base_url, headers, domainName)

                #print("Reponse : "+reponse)
            #Logic to determine host based on Environment
            else:
                print("Pleas Provide Domain Name to Create.")

            print("End Action createDomain")

        if action == 'disableProbes':
            # Call Function disableProbes()
            print("Start Action disableProbes")
            #disable_probes(hosts, port, username, password)
            print("End Action disableProbes")

        if action == 'checkProbeStatus':
            # Call Function checkProbeStatus()
            print("Start Action checkProbeStatus")
            check_probe_status(base_url, headers, host)
            print("End Action checkProbeStatus")

        if action == 'OtherAction':
            # Call Function OtherAction()
            print("Start Action OtherAction")
            #disable_probes(hosts, port, username, password)
            print("End Action OtherAction")

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some integers.')
    parser.add_argument('-env', required=True, help='Environment name')
    parser.add_argument('-host', required=False, help='DataPower Host name')
    parser.add_argument('-action', required=True, help='Action name')
    parser.add_argument('-objectName', required=False, help='Object name')
    parser.add_argument('-domainName', required=False, help='Application Domain name')

    # Log the execution
    args = parser.parse_args()
    username = os.getenv('USER') or os.getenv('USERNAME')
    command = f"{username} : python dpops.py -env {args.env} -action {args.action} -host {args.host} -objectName {args.objectName} -domainName {args.domainName}"
    logging.info(command)

    env = ''
    action = ''
    host = ''
    port = '5551'
    username = ''
    password = ''
    objectName = ''
    domainName = ''

    environments = {
        'sbx':['sbxhost1.mydomain.com'],
        'dev':['devhost1.mydomain.com'],
    }

    actions = [
    'getDomainsList',
    'createDomain',
    'disableProbes',
    'checkDomainsExistance',
    'checkProbeStatus',
    'listObjects_down',
    'getObjectStatus'
    ]

    dpOperations(hosts, port, username, password, action, objectName, domainName)

