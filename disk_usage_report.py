import smtplib
import subprocess
from email.mime.text import MIMEText
import socket

def get_disk_space(path):
    # Run the df command and capture its output
    df_process = subprocess.Popen(['df', '-h', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    df_output, df_error = df_process.communicate()

    if df_process.returncode == 0:
        return df_output.decode('utf-8')
    else:
        return f"Error running df command:\n{df_error.decode('utf-8')}"

def send_email(sender_email, sender_password, recipient_email, subject, message, smtp_server, smtp_port):
    # Set up the MIMEText object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to the SMTP server using the provided server and port
    server = smtplib.SMTP(smtp_server, smtp_port)

    # Identify the client to the server
    server.ehlo()

    # Start a secure TLS connection
    server.starttls()

    # Commented out: Log in to the email account (not required for some servers)
    # server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Disconnect from the SMTP server
    server.quit()

if __name__ == "__main__":
    # Set your email, path, and SMTP information
    server_name = socket.gethostname()
    sender_email = 'info@gmail.com'
    sender_password = 'your_email_password'
    recipient_email = 'anil.kolla@gmail.com'
    path = '/data/secure'
    smtp_server = 'smtp.gmail.com'  # Corrected SMTP server address for Gmail
    smtp_port = 587  # Gmail typically uses port 587 for TLS

    # Create the email subject with the server name
    subject = f'Disk Space Report - Server: {server_name}'

    disk_space_info = get_disk_space(path)

    # Create the email message
    message = f"Disk space report for path '{path}' on server '{server_name}':\n{disk_space_info}"

    # Send the email without login (if not required)
    send_email(sender_email, sender_password, recipient_email, subject, message, smtp_server, smtp_port)
