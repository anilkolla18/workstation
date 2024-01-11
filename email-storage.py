import smtplib
import subprocess
from email.mime.text import MIMEText

def get_disk_space(path):
    # Run the df command and capture its output
    df_process = subprocess.Popen(['df', '-h', path], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    df_output, df_error = df_process.communicate()

    if df_process.returncode == 0:
        return df_output.decode('utf-8')
    else:
        return f"Error running df command:\n{df_error.decode('utf-8')}"

def send_email(sender_email, sender_password, recipient_email, subject, message):
    # Set up the MIMEText object
    msg = MIMEText(message)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = recipient_email

    # Connect to the SMTP server
    server = smtplib.SMTP('smtp.yourprovider.com', 587)  # Use your email provider's SMTP server and port
    server.starttls()

    # Log in to the email account
    server.login(sender_email, sender_password)

    # Send the email
    server.sendmail(sender_email, recipient_email, msg.as_string())

    # Disconnect from the SMTP server
    server.quit()

if __name__ == "__main__":
    # Set your email and path information
    sender_email = 'your_email@gmail.com'
    sender_password = 'your_email_password'
    recipient_email = 'recipient_email@example.com'
    subject = 'Disk Space Report'

    path = '/data/secure'
    disk_space_info = get_disk_space(path)

    # Create the email message
    message = f"Disk space report for path '{path}':\n{disk_space_info}"

    # Send the email
    send_email(sender_email, sender_password, recipient_email, subject, message)
