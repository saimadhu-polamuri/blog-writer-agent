
import smtplib
from email.message import EmailMessage

class Email():

    def send_email_with_attachment( self, sender, recipient, subject, body, attachment_path, smtp_server, smtp_port, login, password):
        """
        Send an email with the specified PDF attachment.
        """
        msg = EmailMessage()
        msg["Subject"] = subject
        msg["From"] = sender
        msg["To"] = recipient
        msg.set_content(body)

        # Attach the PDF file
        with open(attachment_path, "rb") as f:
            file_data = f.read()
        msg.add_attachment(
        file_data,
        maintype="application",
        subtype="pdf",
        filename=os.path.basename(attachment_path))

        with smtplib.SMTP_SSL(smtp_server, smtp_port) as smtp:
            smtp.login(login, password)
            smtp.send_message(msg)
