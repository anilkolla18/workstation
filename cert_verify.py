#!/usr/bin/env python3

import subprocess
import base64
import tempfile
import os
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# Config
DAYS_THRESHOLD = 90
REPORT_FILE = "/tmp/k8s-cert-report.txt"
EXPIRING_FILE = "/tmp/k8s-cert-expiring.txt"
EMAIL_RECIPIENT = "your_email@example.com"
EMAIL_SUBJECT = f"Kubernetes TLS Cert Expiry Report (Next {DAYS_THRESHOLD} Days)"
SMTP_SERVER = "localhost"  # or your SMTP host

# Helper to run shell commands
def run_cmd(cmd):
    result = subprocess.run(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout.strip()

# Initialize report files
with open(REPORT_FILE, 'w') as rf:
    rf.write(f"Cert Expiry Report - Generated on {datetime.now()}\n")
    rf.write("=" * 60 + "\n")

with open(EXPIRING_FILE, 'w') as ef:
    pass  # just create/empty the file

# Get all secret names
secret_names = run_cmd("kubectl get secrets -o jsonpath='{.items[*].metadata.name}'").split()

for secret in secret_names:
    try:
        # Check if tls.crt exists
        secret_data = run_cmd(f"kubectl get secret {secret} -o jsonpath='{{.data}}'")
        if 'tls.crt' not in secret_data:
            continue

        # Get the base64-encoded cert
        encoded_crt = run_cmd(f"kubectl get secret {secret} -o jsonpath='{{.data.tls\\.crt}}'")
        if not encoded_crt:
            continue

        # Decode and write to a temp file
        decoded_crt = base64.b64decode(encoded_crt.encode('utf-8'))
        with tempfile.NamedTemporaryFile(delete=False) as tmp_cert:
            tmp_cert.write(decoded_crt)
            tmp_cert_path = tmp_cert.name

        # Get expiration date using openssl
        expiration_str = run_cmd(f"openssl x509 -enddate -noout -in {tmp_cert_path}")
        os.unlink(tmp_cert_path)
        if not expiration_str.startswith("notAfter="):
            continue

        expiration_date = datetime.strptime(expiration_str.split("=")[1], "%b %d %H:%M:%S %Y %Z")
        days_remaining = (expiration_date - datetime.now()).days

        line = f"{expiration_date} (in {days_remaining} days) - {secret}"
        with open(REPORT_FILE, 'a') as rf:
            rf.write(line + "\n")

        if days_remaining <= DAYS_THRESHOLD:
            with open(EXPIRING_FILE, 'a') as ef:
                ef.write(line + "\n")

    except Exception as e:
        print(f"Error processing secret {secret}: {e}")
        continue

# Send email if needed
if os.path.getsize(EXPIRING_FILE) > 0:
    with open(EXPIRING_FILE) as ef:
        body = ef.read()

    msg = MIMEText(f"The following Kubernetes TLS certs are expiring within {DAYS_THRESHOLD} days:\n\n{body}")
    msg['Subject'] = EMAIL_SUBJECT
    msg['From'] = "k8s-cert-monitor@yourdomain.com"
    msg['To'] = EMAIL_RECIPIENT

    try:
        with smtplib.SMTP(SMTP_SERVER) as server:
            server.send_message(msg)
        print(f"✅ Email sent to {EMAIL_RECIPIENT}")
    except Exception as e:
        print(f"❌ Failed to send email: {e}")
else:
    print("✅ No certificates expiring within threshold.")
