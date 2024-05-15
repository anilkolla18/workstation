import json
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(subject, message):
    sender_email = "your_email@example.com"  # Replace with your email
    receiver_email = "recipient@example.com"  # Replace with recipient email

    # Create a multipart message and set headers
    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject

    # Add body to email
    msg.attach(MIMEText(message, "plain"))

    # Send email
    with smtplib.SMTP("smtp.example.com") as server:
        server.send_message(msg)

# Load JSON data from file
with open('Domain-status.json') as f:
    data = json.load(f)

probe_enabled_domains = []

# Loop through objects in DomainStatus
for domain_status in data["DomainStatus"]:
    if domain_status["ProbeEnabled"] == "on":
        probe_enabled_domains.append(domain_status["Domain"])

if probe_enabled_domains:
    subject = "Probes are enabled in below Domains"
    message = "Probes are enabled in below Domains, Please make sure to disable them if they are not in Use.\n"
    message += "\n".join(probe_enabled_domains)
else:
    subject = "No Probes were enabled"
    message = "No Probes were enabled. Have a good Work Day :)"

send_email(subject, message)
