# crontab -e
# add below line to run the script every 5 min
# */5 * * * * /usr/bin/python3 /path/to/your/script.py
python pod-monitor.py -action check-pod-status


import argparse
from kubernetes import client, config
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load kubeconfig
config.load_kube_config()

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
    v1 = client.CoreV1Api()
    ret = v1.list_pod_for_all_namespaces(watch=False)

    alert = False
    body = "Pod status alert:\n\n"
    for i in ret.items:
        pod_name = i.metadata.name
        pod_namespace = i.metadata.namespace
        pod_status = i.status.phase
        ready_status = "1/1" if pod_status == "Running" else "0/1" if pod_status == "Succeeded" else "Not Ready"

        # Check if the pod is in the desired state
        if not ((pod_status == "Running" and i.status.container_statuses[0].ready) or (pod_status == "Succeeded")):
            alert = True
            body += f"Pod {pod_name} in namespace {pod_namespace} is in {pod_status} state with READY status {ready_status}\n"

    if alert:
        send_email("Kubernetes Pod Alert", body)

def main(action):
    if action == 'check-pod-status':
        check_pod_status()
    # Add more actions here if needed in the future

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Perform actions related to Kubernetes monitoring.')
    parser.add_argument('-action', choices=['check-pod-status'], required=True, help='Action to perform')

    args = parser.parse_args()
    main(args.action)
