#!/usr/bin/env python3
import smtplib
import ssl
import imaplib
import configparser
import os
import sys
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

try:
    from email_limiter import can_send_to
except ImportError:
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))
    from email_limiter import can_send_to

def send_email_with_attachment(to_email, subject, body, attachment_path):
    config = configparser.ConfigParser()
    config.read('/home/raamuser/email/config.ini')
    
    smtp_server = 'smtp.mailbox.org'
    smtp_port = 587
    sender_email = config.get('imap', 'username')
    password = os.environ.get('OPENCLAW_MAIL_PW')
    if not password:
        with open('/home/raamuser/pw.txt', 'r') as f:
            lines = f.read().splitlines()
            for line in lines:
                if 'mailbox.org' in line or 'Openclaw' in line:
                    password = line.split()[-1]
                    break
        if not password:
            password = 'Openclaw_001' # default fallback
    
    message = MIMEMultipart()
    message['From'] = sender_email
    message['To'] = to_email
    message['Subject'] = subject
    
    message.attach(MIMEText(body, 'plain'))
    
    if os.path.exists(attachment_path):
        with open(attachment_path, "rb") as f:
            attach = MIMEApplication(f.read(), _subtype="mp4")
            attach.add_header('Content-Disposition', 'attachment', filename=os.path.basename(attachment_path))
            message.attach(attach)
    else:
        print(f"Attachment not found: {attachment_path}")
        return

    if not can_send_to(to_email, subject, body):
        print(f"Recipient {to_email} has reached the email limit. Not sending.")
        return
        
    context = ssl.create_default_context()
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls(context=context)
        server.login(sender_email, password)
        msg_string = message.as_string()
        server.sendmail(sender_email, to_email, msg_string)
        server.quit()
        try:
            imap = imaplib.IMAP4_SSL('imap.mailbox.org', 993)
            imap.login(sender_email, password)
            imap.append('Sent', '\\Seen', None, msg_string.encode('utf-8'))
            imap.logout()
        except Exception as ie:
            print(f"Warning: sent but failed to save to Sent folder: {ie}")
        print(f"Email with attachment sent successfully to {to_email}")
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    operator_email = "openclawoperator@mailbox.org"
    mp4_path = "/home/raamuser/mars_breaking_news.mp4"
    subject = "VIDEO UPDATE: Breaking News Mars Landing Found Footage"
    body = "Please find attached the low-res 'found footage' video from the Mars surface, along with the news broadcast."
    
    send_email_with_attachment(operator_email, subject, body, mp4_path)
