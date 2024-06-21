# crontab -e
# add below line to run the script every 5 min
# */5 * * * * /usr/bin/python3 /path/to/your/script.py
#python pod-monitor.py -action check-pod-status

import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, body):
    sender_email = "your_email@example.com"
    receiver_email = "alert_recipient@example.com"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.example.com', 25) as server:
            text = msg.as_string()
            server.sendmail(sender_email, receiver_email, text)
        print("Email sent successfully!")
    except Exception as e:
        print(f"Error sending email: {e}")

def check_pod_status():
    try:
        # Replace with your actual kubectl command to get pod status
        result = subprocess.run(['kubectl', 'get', 'pods', '--all-namespaces', '--output=jsonpath={range .items[*]}{.metadata.name}{"\t"}{.metadata.namespace}{"\t"}{.status.phase}{"\t"}{.status.containerStatuses[*].ready}{"\n"}'], stdout=subprocess.PIPE, check=True, text=True)

        alert = False
        body = "Pod status alert:\n\n"

        for line in result.stdout.strip().split('\n'):
            pod_name, pod_namespace, pod_status, ready_status = line.split('\t')

            # Check if the pod is in the desired state
            if not ((pod_status == "Running" and ready_status == "True") or (pod_status == "Succeeded")):
                alert = True
                body += f"Pod {pod_name} in namespace {pod_namespace} is in {pod_status} state with READY status {ready_status}\n"

        if alert:
            send_email("Kubernetes Pod Alert", body)

    except subprocess.CalledProcessError as e:
        print(f"Error running kubectl command: {e}")

def custom_action():
    # Define your custom action logic here
    print("Performing custom action")

def main(action):
    if action == 'check-pod-status':
        check_pod_status()
    elif action == 'custom-action':
        custom_action()
    # Add more actions as needed

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform actions related to Kubernetes monitoring.')
    parser.add_argument('-action', choices=['check-pod-status', 'custom-action'], required=True, help='Action to perform')

    args = parser.parse_args()
    main(args.action)

