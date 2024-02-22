import requests
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Function to make a REST API call and verify response
def make_rest_call(url, json_data, headers):
    try:
        response = requests.post(url, json=json_data, headers=headers)
        if response.status_code == 200:
            return True, response.text
        else:
            return False, f"Failed to make REST call. Status code: {response.status_code}"
    except Exception as e:
        return False, f"Error making REST call: {str(e)}"

# Function to send email
def send_email(subject, body):
    # Email configurations
    sender_email = "your_email@example.com"
    receiver_email = "recipient_email@example.com"
    smtp_server = "smtp.example.com"
    smtp_port = 587
    smtp_username = "your_smtp_username"
    smtp_password = "your_smtp_password"

    # Create message container
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = receiver_email
    msg['Subject'] = subject

    # Attach message body
    msg.attach(MIMEText(body, 'plain'))

    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, msg.as_string())
        server.quit()
        print("Email sent successfully")
    except Exception as e:
        print(f"Error sending email: {str(e)}")

if __name__ == "__main__":
    # URL to make the REST call
    api_url = "https://api.example.com"

    # JSON data for the POST request
    json_data = {
        "shutdown": {
            "Mode": "reload",
            "Delay": 10
        }
    }

    # Headers for the POST request
    headers = {
        "Authorization": "Bearer your_token_here",
        "Content-Type": "application/json"
    }

    # Make REST call
    success, response = make_rest_call(api_url, json_data, headers)

    if success:
        # If REST call is successful, send success email
        send_email("REST Call Successful", f"Response: {response}")
    else:
        # If REST call fails, send failure email
        send_email("REST Call Failed", f"Error: {response}")
