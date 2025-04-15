#!/usr/bin/env python3

import argparse
import subprocess
import smtplib
from email.mime.text import MIMEText

# Run a shell command and return the output
def run_command(cmd):
    try:
        result = subprocess.run(cmd, shell=True, check=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        return result.stdout
    except subprocess.CalledProcessError as e:
        return f"[ERROR] Command failed:\n{e.output}"

# Send email with command output
def send_email(subject, message, to_email="admin@example.com"):
    from_email = "noreply@example.com"
    msg = MIMEText(message)
    msg["Subject"] = subject
    msg["From"] = from_email
    msg["To"] = to_email

    try:
        with smtplib.SMTP("localhost") as server:
            server.sendmail(from_email, [to_email], msg.as_string())
        print("Email sent.")
    except Exception as e:
        print(f"Email failed: {e}")

# Main logic
def main():
    parser = argparse.ArgumentParser(description="Cluster Monitor Tool")
    parser.add_argument("--action", required=True, choices=["get-pods", "get-mgmt", "health-check"])
    args = parser.parse_args()

    actions = {
        "get-pods": "kubectl get po -A",
        "get-mgmt": "kubectl get mgmt -A",
        "health-check": "apic health-check"
    }

    cmd = actions[args.action]
    output = run_command(cmd)
    print(output)
    send_email(f"Cluster Monitor: {args.action}", output)

if __name__ == "__main__":
    main()
